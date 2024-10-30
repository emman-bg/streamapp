from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('user_profiles/', views.UserProfileGetFilter.as_view()),
    path('user_profile/<int:pk>', views.UserProfileCreateUpdateDelete.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)