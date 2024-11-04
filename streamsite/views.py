from rest_framework import generics

from .models import *
from .serializers import *


class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.filter(is_active=True)
    serializer_class = UserProfileSerializer


class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.filter(is_active=True)
    serializer_class = UserProfileCreateSerializer


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.filter(is_active=True)
    serializer_class = UserProfileUpdateSerializer


class ChannelListView(generics.ListCreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class ChannelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class SubscriptionListView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class VideoListView(generics.ListCreateAPIView):
    queryset = Video.objects.filter(removed=False)
    serializer_class = VideoSerializer


class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class ContentListView(generics.ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer


class ContentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer