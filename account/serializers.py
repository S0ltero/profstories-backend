from django.contrib.auth import get_user_model

from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer

from .models import Employer, Professional

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("password", "last_login", "date_joined", 
                   "is_superuser", "is_staff", "is_active", 
                   "groups", "user_permissions")


class CreateUserSerializer(DjoserUserCreateSerializer):

    class Meta:
        model = User
        exclued = ("last_login", "date_joined",
                   "is_superuser", "is_staff", "is_active", 
                   "groups", "user_permissions")

