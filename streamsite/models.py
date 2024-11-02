from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime, timedelta
from simple_history.models import HistoricalRecords


FREE_TRIAL_PERIOD = datetime.now() + timedelta(days=7)


class UserProfile(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True, max_length=30)

    def __str__(self):
        return self.username

    @property
    def subscriptions(self):
        return self.subscriptions
    
    @property
    def is_creator(self):
        return Channel.objects.filter(owner=self).exists()


class Channel(models.Model):
    name = models.CharField(max_length=30)
    owner = models.OneToOneField(
        UserProfile, related_name='channel',
        on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def contents(self):
        return self.contents


class Subscription(models.Model):
    WEEKLY = 0
    MONTHLY = 1
    QUARTERLY = 2
    YEARLY = 3
    SUBSCRIPTION_TYPE_CHOICES = (
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (QUARTERLY, 'Quarterly'),
        (YEARLY, 'Yearly'),
    )

    payor = models.ForeignKey(
        UserProfile, related_name='purchases',
        null=True, blank=True, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(
        UserProfile, related_name='subscriptions',
        null=True, blank=True, on_delete=models.CASCADE)
    subscription_type = models.IntegerField(
        choices=SUBSCRIPTION_TYPE_CHOICES, default=WEEKLY)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=FREE_TRIAL_PERIOD)
    channel = models.ForeignKey(Channel, null=True, blank=True, on_delete=models.SET_NULL)
    subscription_history = HistoricalRecords()

    @property
    def subscription_type_display(self):
        return self.get_subscription_type_display()

    @property
    def username(self):
        return self.user_profile.username


class Video(models.Model):
    file = models.FileField(upload_to='./videos')
    thumbnail = models.ImageField(upload_to='./thumbnails', blank=True, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(default=timedelta)
    uploaded_by = models.ForeignKey(
        UserProfile, related_name='videos', on_delete=models.CASCADE)
    removed = models.BooleanField(default=False)


class Content(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=2000)
    posted_on = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(
        UserProfile, related_name='contents', on_delete=models.CASCADE)
    channel = models.ForeignKey(
        Channel, related_name='contents', on_delete=models.CASCADE)
    views = models.PositiveBigIntegerField(default=0)
    likes = models.PositiveBigIntegerField(default=0)