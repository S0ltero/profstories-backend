import string

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.contrib.auth.base_user import BaseUserManager

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from djoser.serializers import UserCreatePasswordRetypeSerializer as DjoserUserCreateSerializer

from helper.serializers import SkillSerializer
from .models import (
    Employer,
    Professional,
    NPO,
    College,
    EmploymentAgency,
    Teacher,
    Student,
    Upload,
    Callback
)

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
                data.update(EmployerDetailSerializer(employer).data)
        elif instance.type == User.Types.PROFESSIONAL:
            try:
                professional = Professional.objects.get(pk=instance.id)
            except Professional.DoesNotExist:
                pass
            else:
                data.update(ProfessionalDetailSerializer(professional).data)
        elif instance.type == User.Types.COLLEGE:
            try:
                college = College.objects.get(pk=instance.id)
            except College.DoesNotExist:
                pass
            else:
                data.update(CollegeDetailSerializer(college).data)
        elif instance.type == User.Types.EMPAGENCY:
            try:
                empagency = EmploymentAgency.objects.get(pk=instance.id)
            except EmploymentAgency.DoesNotExist:
                pass
            else:
                data.update(EmploymentAgencySerializer(empagency).data)
        return data


class CreateUserSerializer(DjoserUserCreateSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=False)

    class Meta:
        model = User
        exclude = ("last_login", "date_joined",
                   "is_superuser", "is_staff", "is_active", 
                   "groups", "user_permissions")

    def validate(self, attrs):
        if attrs.get("type") and not attrs.get("password"):
            if attrs["type"] == User.Types.TEACHER:
                attrs["password"] = BaseUserManager().make_random_password()
            else:
                raise ValidationError(detail={"password": "Поле не может быть пустым!"})
        elif not attrs.get("password"):
            raise ValidationError(detail={"password": "Поле не может быть пустым!"})
        return super().validate(attrs)


class EmployerSerializer(serializers.ModelSerializer):
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
        fields = "__all__"


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


class EmploymentAgencySerializer(serializers.ModelSerializer):

    class Meta:
        model = EmploymentAgency
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = "__all__"

    def save(self, **kwargs):
        code = get_random_string(6, allowed_chars=string.ascii_uppercase + string.digits)
        return super().save(**kwargs, code=code)


class StudentEmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ("pk", "company_name_other", "company_logo")


class StudentProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ("pk", "speciality")


class StudentSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    middle_name = serializers.CharField(source="user.middle_name", read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Student
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
