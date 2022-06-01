from django.urls import path

from .views import UploadVideo, PersonalDataView, AcademicList, AcademicDetail

urlpatterns=[
    path('presentation/', UploadVideo.as_view(), name = "presentation-video"),
    path('personal-data/', PersonalDataView.as_view(), name = "personal-data"),
    # path('academic-data/', AcademicDataView.as_view(), name = "academic-data"),
    path('academic-data/', AcademicList.as_view()),
    path('academic-data/<int:pk>/', AcademicDetail.as_view()),
    # path('interest-profile/', InterestProfileView.as_view(), name = "interest-profile"),


]