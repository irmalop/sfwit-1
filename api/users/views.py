from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, ResendSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.shortcuts import redirect, render
# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class=RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')

        absurl='http://'+ current_site + relativeLink + "?token="+ str(token)
        email_body = 'Hi ' + user.email + ' Use link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

class  VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY)
            user = User.objects.get(id = payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return redirect('/auth/login/')
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class  LoginAPIView(generics.GenericAPIView):
    serializer_class= LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
class ResendVerifyEmail(generics.GenericAPIView):
    serializer_class = ResendSerializer
    def post(self, request):
        data = request.data
        # email = data.get('email')
        email = data['email']
        try:
            user = User.objects.get(email=email)
       
            if user.is_verified:
                return Response({'msg':'User is already verified'})
            token = RefreshToken.for_user(user).access_token
            current_site= get_current_site(request).domain
            relativeLink = reverse('email-verify')
            
            absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
            email_body = 'Hi '+ user.email + ' this is the resent link to verify your email \n' + absurl

            data = {'email_body':email_body,'to_email':user.email,
                    'email_subject':'Verify your email'}
            Util.send_email(data)
            return Response({'msg':'The verification email has been sent'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'msg':'No such user, register first'})