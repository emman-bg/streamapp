from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *


class UserProfileGetFilter(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileCreateUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
