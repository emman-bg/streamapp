from .models import *

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_profile'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'pk',
            'username',
            'email',
            'is_active',
            'is_staff',
            'is_superuser'
        ]
        read_only_fields = fields

class UserProfileCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'email',
            'password',
            'password_confirm',
            'is_active',
            'is_staff',
            'is_superuser'
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                "Passwords do not match."
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = UserProfile.objects.create_user(
            password=password, **validated_data)
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False)
    new_password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            'new_password',
            'new_password_confirm'
        ]

    def validate(self, data):
        if 'new_password' in data and\
            data['new_password'] != data.get('new_password_confirm'):
            raise serializers.ValidationError(
                "New passwords do not match."
            )
        return data

    def update(self, instance, validated_data):
        new_password = validated_data.pop(
            'new_password', None)
        validated_data.pop('new_password_confirm', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance


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
            'payor',
            'subscriber',
            'subscription_type',
            'start_date',
            'end_date',
            'channel'
        ]


class VideoSerializer(serializers.ModelSerializer):
    uploaded_by = UserProfileSerializer()

    class Meta:
        model = Video
        fields = [
            'file',
            'thumbnail',
            'date_uploaded',
            'duration',
            'uploaded_by',
            'removed'
        ]


class ContentSerializer(serializers.ModelSerializer):
    posted_by = UserProfileSerializer()
    channel = ChannelSerializer()

    class Meta:
        model = Content
        fields = [
            'title',
            'description',
            'posted_on',
            'posted_by',
            'channel',
            'views'
        ]
