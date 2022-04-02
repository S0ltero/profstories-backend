from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Event

User = get_user_model()


class EventSerialzier(serializers.ModelSerializer):
    organizer = serializers.SerializerMethodField()

    def get_organizer(self, obj):
        if obj.user.type == User.Types.EMPLOYER:
            organizer = obj.user.employer.company_name
        elif obj.user.type == User.Types.COLLEGE:
            organizer = obj.user.college.college_name
        elif obj.user.type == User.Types.NPO:
            organizer = obj.user.npo.company_name

        return organizer

    class Meta:
        model = Event
        fields = "__all__"


class EventStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            "title_other", "description_other", "format_other",
            "address_other", "audience_level_other", "mode", 
            "date", "is_free",)


class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"


class EventDetailSerializer(serializers.ModelSerializer):
    organizer = serializers.SerializerMethodField()

    def get_organizer(self, obj):
        if obj.user.type == User.Types.EMPLOYER:
            organizer = obj.user.employer.company_name
        elif obj.user.type == User.Types.COLLEGE:
            organizer = obj.user.college.college_name
        elif obj.user.type == User.Types.NPO:
            organizer = obj.user.npo.company_name

        return organizer

    class Meta:
        model = Event
        fields = "__all__"