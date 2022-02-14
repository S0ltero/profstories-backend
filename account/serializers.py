from django.contrib.auth import get_user_model

from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer

from .models import Employer, Professional

User = get_user_model()

