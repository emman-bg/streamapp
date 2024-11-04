from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views


urlpatterns = [
	path('login/', TokenObtainPairView.as_view()),
    path('user_profiles/', views.UserProfileListView.as_view()),
    path('user_profile/create/', views.UserProfileCreateView.as_view()),
    path('user_profile/<int:pk>', views.UserProfileDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)