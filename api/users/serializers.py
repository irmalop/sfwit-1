from asyncore import write
from logging import raiseExceptions
from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed

from django.contrib import auth

from .models import FailedAttempt

special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"


class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=60, min_length=6, write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(max_length=60, min_length=6, write_only=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['email', 'password', 'password2'
        , 'is_applicant', 'is_employer'
        # , 'user_type'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def save(self):
        user = User(
            email = self.validated_data['email'],
            # user_type=self.validated_data['user_type']
            is_applicant = self.validated_data['is_applicant'],
            is_employer = self.validated_data['is_employer'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match'})
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password')

        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least 1 digit.')
        if not any(char.isalpha() for char in password):
            raise ValidationError('Password must contain at least 1 letter.') 
        if not any(char in special_characters for char in password):
            raise ValidationError('Password must contain at least 1 special character.')
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least 1 uppercase.')
        # user_type = attrs.get('user_type', '')

        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class  EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

class  LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255, min_length = 3)
    password = serializers.CharField(max_length=20, min_length = 6, write_only = True, style={'input_type': 'password'})
    tokens_refresh = serializers.CharField(max_length=68, min_length = 6, read_only = True)
    tokens_access = serializers.CharField(max_length=68, min_length = 6, read_only = True)
    is_applicant = serializers.BooleanField(read_only = True)
    is_employer = serializers.BooleanField(read_only = True)
    # tokens = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['email', 'password', 'tokens_refresh', 'tokens_access', 'id','is_applicant', 'is_employer']
    # def get_tokens(self, obj):
    #     return User.tokens(User)
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        # import pdb
        # pdb.set_trace()


        if not user:

            raise AuthenticationFailed('Invalid credential, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'tokens_refresh': user.tokens_refresh(),
            'tokens_access': user.tokens_access(),
            'id': user.id,
            'is_applicant': user.is_applicant,
            'is_employer': user.is_employer
        }
    def monitor_login( auth_func ):
        """
        Function that replaces Django authentication() function with one that tracks failed logins and blocks further attempts based on a threshold
        """
        if hasattr( auth_func, '__PROTECT_FAILED_LOGINS__' ) :
        # avoiding multiple decorations
            return auth_func
    
        def decorate( *args, **kwargs ):
            """ Wrapper for Django authentication function """
            user = kwargs.get( 'email', '' )
            if not user:
                raise ValueError( 'username must be supplied by the \
                authentication function for FailedLoginBlocker to operate' )
                
            try:
                fa = FailedAttempt.objects.get( email=user )
                if fa.recent_failure( ):
                    if fa.too_many_failures( ):
                        # block the authentication attempt because
                        # of too many recent failures
                        fa.failures += 1
                        fa.save( )
                        raise ValidationError({'email': 'Your account has been locked due to too many failed login attempts.'})
                else:
                    # the block interval is over, reset the count
                    fa.failures = 0
                    fa.save( )
            except FailedAttempt.DoesNotExist:
                fa = None

            result = auth_func( *args, **kwargs )
            if result:
                # the authentication was successful
                return result
            # authentication failed 
            fa = fa or FailedAttempt( email=user, failures=0 )
            fa.failures += 1
            fa.save( )
            # return with unsuccessful auth
            return None

        decorate.__PROTECT_FAILED_LOGINS__ = True
        return decorate
    auth.authenticate = monitor_login( auth.authenticate )

class  ResendSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255, min_length = 3)

    class Meta:
        model = User
        fields = ['email']
