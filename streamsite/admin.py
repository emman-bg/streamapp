from django.contrib import admin
from .models import *


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date')
