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


class EmployerSerialzier(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name")
    first_name = serializers.CharField(source="user.first_name")
    middle_name = serializers.CharField(source="user.middle_name")

    class Meta:
        model = Employer
        fields = ("company_logo", "company_name", "company_region",
                  "last_name", "first_name", "middle_name")


class EmployerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ("company_logo", "company_name", "company_region")


class EmployerDetailSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name")
    first_name = serializers.CharField(source="user.first_name")
    middle_name = serializers.CharField(source="user.middle_name")

    class Meta:
        model = Employer
        fields = "__all__"


class ProfessionalSerialzier(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name")
    first_name = serializers.CharField(source="user.first_name")
    middle_name = serializers.CharField(source="user.middle_name")

    class Meta:
        model = Professional
        fields = ("photo", "company_name", "region", "speciality")
