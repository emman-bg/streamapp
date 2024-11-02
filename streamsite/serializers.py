from rest_framework import serializers
from .models import *



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'subscriptions', 'is_creator']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['name', 'owner', 'date_created']


class SubscriptionSerializer(serializers.ModelSerializer):
    payor = UserProfileSerializer()
    subscriber = UserProfileSerializer()
    channel = ChannelSerializer()

    class Meta:
        model = Subscription
        fields = [
            'payor', 'subscriber', 'subscription_type',
            'start_date', 'end_date', 'channel'
        ]


class VideoSerializer(serializers.ModelSerializer):
    uploaded_by = UserProfileSerializer()

    class Meta:
        model = Video
        fields = [
            'file', 'thumbnail', 'date_uploaded',
            'duration', 'uploaded_by', 'removed'
        ]


class ContentSerializer(serializers.ModelSerializer):
    posted_by = UserProfileSerializer()
    channel = ChannelSerializer()

    class Meta:
        model = Content
        fields = [
            'title', 'description', 'posted_on',
            'posted_by', 'channel', 'views'
        ]
