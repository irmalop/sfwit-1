from rest_framework import serializers
from users.models import User
from .models import ApplicantVideo, PersonalData, MARITAL_STATUS, AcademicData, SEX
#  InterestProfile, Area, Role, TYPE_JOB, MODALITY
from urllib.parse import urlparse
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class ApplicantVideoSerializer(serializers.ModelSerializer):
    user = User.objects.filter(is_applicant=True)
    user= serializers.PrimaryKeyRelatedField(read_only=True,) 
    video= serializers.URLField(required = True)
    class Meta:
        model = ApplicantVideo
        fields = '__all__'
    def validate_website_url(video):
        '''Validate website into valid URL'''
        msg = "Cannot validate this website: %s" % video
        validate = URLValidator(message=msg)
        try:
            validate(video)
        except:
            o = urlparse.urlparse(video)
            if o.path:
                path = o.path
                while path.endswith('/'):
                    path = path[:-1]
                path = "http://"+path
                validate(path)
                return path
            else:
                raise ValidationError(message=msg)
        return video
class PersonalDataSerializer(serializers.ModelSerializer):
    user = User.objects.filter(is_applicant=True)
    user= serializers.PrimaryKeyRelatedField(read_only=True,) #by default allow_null = False
    name = serializers.CharField(required = True, max_length=40)
    fathers_surname = serializers.CharField(required = True, max_length=40)
    mothers_surname = serializers.CharField(required = True, max_length=40)
    sexo = serializers.ChoiceField(choices=SEX)
    birth_date = serializers.DateField(required = True)
    marital_status = serializers.ChoiceField(choices = MARITAL_STATUS)
    age = serializers.IntegerField(required = True, validators=[MinValueValidator(18), MaxValueValidator(80)])
    email = serializers.EmailField(max_length = 100, min_length = 3)
    state = serializers.CharField(required = True, max_length=50)
    municipality = serializers.CharField(required = True, max_length=50)
    class Meta:
        model = PersonalData
        fields = '__all__'
# class AcademicDataSerializer(serializers.ModelSerializer):
#     user = User.objects.filter(is_applicant=True)
#     user= serializers.PrimaryKeyRelatedField(many=True, read_only=True) #by default allow_null = False
#     level = serializers.ChoiceField(choices=LEVEL)
#     name = serializers.CharField(required = True, max_length=50)
#     institution = serializers.CharField(required = True, max_length=50)
#     duration = serializers.CharField(required = True, max_length=50)
#     status = serializers.ChoiceField(choices=STATUS)
#     class Meta:
#         model = AcademicData
#         fields = '__all__'   
# class InterestProfileSerializer(serializers.ModelSerializer):
#     user = User.objects.filter(is_applicant=True)
#     user= serializers.PrimaryKeyRelatedField(read_only=True,)
#     area = serializers.PrimaryKeyRelatedField(queryset=Area.objects.all())
#     role = serializers.PrimaryKeyRelatedField(many=True, queryset=Role.objects.all()) # all objects for now
#     modality = serializers.ChoiceField(choices=MODALITY)
#     type_job = serializers.ChoiceField(choices=TYPE_JOB)

#     class Meta:
#         model = InterestProfile
#         fields = '__all__'
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance:
#             self.fields['role'].queryset = instance.area.role.all()
from .models import AcademicData

class AcademicDataSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = AcademicData
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    academic = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'academic']