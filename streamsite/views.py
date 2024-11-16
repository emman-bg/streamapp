from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import *
from .serializers import *


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.filter(removed=False)
    serializer_class = UserProfileCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username, access_token, refresh_token = serializer.save()

        return Response({
            'username': username,
            'access': access_token,
            'refresh': refresh_token
        }, status=status.HTTP_201_CREATED)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.filter(removed=False)
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