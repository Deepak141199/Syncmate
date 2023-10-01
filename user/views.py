from rest_framework import generics, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer
from django.db import models
from django.contrib.auth.models import AbstractUser

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny  # Allow anyone to register
    ]
    serializer_class = UserSerializer

class CustomAuthToken(ObtainAuthToken):
    # Use custom authentication view if needed
    pass

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
