from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime, timedelta
from simple_history.models import HistoricalRecords

SUBSCRIPTION_DURATIONS = [
    timedelta(days=3),  # free trial
    timedelta(days=7),  # weekly
    timedelta(days=30),  # monthly
    timedelta(days=120),  # quarterly
    timedelta(days=365),  # annually
]

class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None, **user_fields):
        print(self, email, username, password, user_fields)
        if not email:
            raise ValueError("Email field is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **user_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **user_fields):
        user_fields.setdefault("is_staff", True)
        user_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **user_fields)


class UserProfile(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True, max_length=30)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)
    user_profile_history = HistoricalRecords()

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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
    is_active = models.BooleanField(default=True)
    channel_history = HistoricalRecords()

    @property
    def contents(self):
        return self.contents


class Subscription(models.Model):
    FREE_TRIAL = 0
    WEEKLY = 1
    MONTHLY = 2
    QUARTERLY = 3
    YEARLY = 4
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
    end_date = models.DateTimeField(null=True, blank=True)
    channel = models.ForeignKey(Channel, null=True, blank=True, on_delete=models.SET_NULL)
    subscription_history = HistoricalRecords()

    @property
    def subscription_type_display(self):
        return self.get_subscription_type_display()

    @property
    def username(self):
        return self.user_profile.username

    def save(self, *args, **kwargs):
        subscription_type = kwargs.get('subscription_type', None)
        if subscription_type:
            self.end_date =\
                datetime.now() + SUBSCRIPTION_DURATIONS[subscription_type]
        super(Subscription, self).save(*args, **kwargs)


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
    removed = models.BooleanField(default=False)
    views = models.PositiveBigIntegerField(default=0)
    likes = models.PositiveBigIntegerField(default=0)
    content_history = HistoricalRecords()