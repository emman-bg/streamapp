from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from streamsite.views import *


urlpatterns = [
	path('login/', CustomTokenObtainPairView.as_view()),
    path('create-account/', UserProfileCreateView.as_view()),
    path('user_profile/<int:pk>', UserProfileDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)