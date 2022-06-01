from django.urls import path
from .views import RegisterView, VerifyEmail, LoginAPIView, ResendVerifyEmail
urlpatterns=[
    path('signup/', RegisterView.as_view(), name = "register"),
    path('login/', LoginAPIView.as_view(), name = "login"), 
    path('email-verify/', VerifyEmail.as_view(), name = "email-verify"),
    path('resend-email-verify/', ResendVerifyEmail.as_view(), name = "resend-email-verify"),
]