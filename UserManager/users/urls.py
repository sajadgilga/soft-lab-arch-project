from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import ProfileView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('register/', TokenObtainPairView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
