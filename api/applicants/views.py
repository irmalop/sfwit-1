from logging import raiseExceptions
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import ApplicantVideoSerializer, PersonalDataSerializer, AcademicDataSerializer
from .models import ApplicantVideo, PersonalData, AcademicData
from users.models import User

# Create your views here.
class  UploadVideo(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        if not ApplicantVideo.objects.filter(user_id=request.user).exists():
            if request.user.is_applicant: 
                serializer = ApplicantVideoSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save(user=request.user) # <---- INCLUDE REQUEST
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'msg':'No such applicant'},status=status.HTTP_401_UNAUTHORIZED)   
        else:
            return Response({'msg':'Already exists'}, status=status.HTTP_400_BAD_REQUEST)   
    def put(self, request):
        serializer = ApplicantVideoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        video = serializer.data["video"]
        user_id = request.user.id   
        presentation = ApplicantVideo.objects.get(user_id=user_id)
        if presentation.video != video:
            presentation.video = video
            presentation.save()
            return Response({'msg': 'Updated succesfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'The link is the same'}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        if ApplicantVideo.objects.filter(user_id=request.user).exists():
            user = ApplicantVideo.objects.get(user_id=request.user)
            serializer = ApplicantVideoSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'msg':'Not found'}, status=status.HTTP_400_BAD_REQUEST)
class  PersonalDataView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        if not PersonalData.objects.filter(user_id=request.user).exists():
            if request.user.is_applicant: 
                serializer = PersonalDataSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save(user=request.user) # <---- INCLUDE REQUEST
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                    # return Response({'msg':'Some field is not valid'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg':'No such applicant'},status=status.HTTP_401_UNAUTHORIZED)   
        else:
            return Response({'msg':'Already exists'}, status=status.HTTP_400_BAD_REQUEST)   
    def get(self, request):
        if PersonalData.objects.filter(user_id=request.user).exists():
            user = PersonalData.objects.get(user_id=request.user)
            serializer = PersonalDataSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'msg':'Not found'}, status=status.HTTP_400_BAD_REQUEST)

# class  AcademicDataView(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated, )
#     def post(self, request):
#         if request.user.is_applicant: 
#             serializer = AcademicDataSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 user = serializer.save(user=request.user) # <---- INCLUDE REQUEST
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#                 # return Response({'msg':'Some field is not valid'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({'msg':'No such applicant'},status=status.HTTP_401_UNAUTHORIZED)      
#     def get(self, request):
#         if AcademicData.objects.filter(user_id=request.user).exists():
#             user = AcademicData.objects.get(user_id=request.user)
#             serializer =AcademicDataSerializer(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({'msg':'Not found'}, status=status.HTTP_400_BAD_REQUEST)

# class  InterestProfileView(generics.GenericAPIView):
#     permission_classes = (IsAuthenticated, )
#     def post(self, request):
#         if not InterestProfile.objects.filter(user_id=request.user).exists():
#             if request.user.is_applicant: 
#                 serializer = InterestProfileSerializer(data=request.data)
#                 if serializer.is_valid(raise_exception=True):
#                     user = serializer.save(user=request.user) # <---- INCLUDE REQUEST
#                     return Response(serializer.data, status=status.HTTP_201_CREATED)
#                     # return Response({'msg':'Some field is not valid'}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'msg':'No such applicant'},status=status.HTTP_401_UNAUTHORIZED)   
#         else:
#             return Response({'msg':'Already exists'}, status=status.HTTP_400_BAD_REQUEST)   
class AcademicList(generics.ListCreateAPIView):
    queryset = AcademicData.objects.all()
    serializer_class = AcademicDataSerializer
    permission_classes = (IsAuthenticated, )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AcademicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AcademicData.objects.all()
    serializer_class = AcademicDataSerializer
    permission_classes = (IsAuthenticated, )