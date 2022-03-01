from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer

from .models import Employer, Professional, NPO, College, Upload, Callback

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ("password", "last_login", "date_joined",
                   "is_superuser", "is_staff", "is_active",
                   "groups", "user_permissions")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.type == User.Types.EMPLOYER:
            try:
                employer = Employer.objects.get(pk=instance.id)
            except Employer.DoesNotExist:
                pass
            else:
                data.update(EmployerSerialzier(employer).data)
        elif instance.type == User.Types.PROFESSIONAL:
            try:
                professional = Professional.objects.get(pk=instance.id)
            except Professional.DoesNotExist:
                pass
            else:
                data.update(ProfessionalSerialzier(professional).data)
        return data


class CreateUserSerializer(DjoserUserCreateSerializer):

    class Meta:
        model = User
        exclude = ("last_login", "date_joined",
                   "is_superuser", "is_staff", "is_active", 
                   "groups", "user_permissions")


class EmployerSerialzier(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user.id")

    class Meta:
        model = Employer
        fields = ("id", "company_logo", "company_name", "company_region")


class EmployerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = "__all__"


class EmployerDetailSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name")
    first_name = serializers.CharField(source="user.first_name")
    middle_name = serializers.CharField(source="user.middle_name")

    class Meta:
        model = Employer
        fields = "__all__"


class ProfessionalSerialzier(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user.id")
    last_name = serializers.CharField(source="user.last_name")
    first_name = serializers.CharField(source="user.first_name")
    middle_name = serializers.CharField(source="user.middle_name")

    class Meta:
        model = Professional
        fields = ("id", "photo", "company_name", "region", "speciality",
                  "last_name", "first_name", "middle_name")


class ProfessionalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = "__all__"


class ProfessionalDetailSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name")
    first_name = serializers.CharField(source="user.first_name")
    middle_name = serializers.CharField(source="user.middle_name")
    workplace_photo = serializers.SerializerMethodField()

    def get_workplace_photo(self, obj):
        uploads = Upload.objects.filter(user_id=obj.user.id, type="workplace")
        return (obj.file.url for obj in uploads)

    class Meta:
        model = Professional
        fields = "__all__"


class NPOSerializer(serializers.ModelSerializer):

    class Meta:
        model = NPO
        fields = ("company_logo", "company_name", "company_region")


class NPOCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPO
        fields = "__all__"


class NPODetailSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name")
    first_name = serializers.CharField(source="user.first_name")
    middle_name = serializers.CharField(source="user.middle_name")

    class Meta:
        model = NPO
        fields = "__all__"


class CollegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = College
        fields = ("company_logo", "company_name", "company_region")


class CollegeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = "__all__"


class CollegeDetailSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(source="user.last_name")
    first_name = serializers.CharField(source="user.first_name")
    middle_name = serializers.CharField(source="user.middle_name")

    class Meta:
        model = College
        fields = "__all__"


class TokenSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="user.id")
    auth_token = serializers.CharField(source="key")
    type = serializers.CharField(source="user.type")
    verification = serializers.CharField(source="user.verification")

    class Meta:
        model = Token
        fields = ("id", "auth_token", "type", "verification")


class CallbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Callback
        fields = "__all__"
