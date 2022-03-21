from rest_framework import serializers

from .models import StudentSkill, StudentMission, Mission, MissionQuestion


class SkillSerializer(serializers.ModelSerializer):
    percent = serializers.SerializerMethodField()
    object = serializers.CharField(source="get_object_display")

    class Meta:
        model = StudentSkill
        fields = ("percent", "object")

    def get_percent(self, obj):
        return 100 * (obj.points / 12)
