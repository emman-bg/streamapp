from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('user_profiles/', views.UserProfileListView.as_view()),
    path('user_profile/create/', views.UserProfileCreateView.as_view()),
    path('user_profile/<int:pk>', views.UserProfileDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)