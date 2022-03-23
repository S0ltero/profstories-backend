from rest_framework import serializers

from .models import StudentSkill, StudentMission, Mission, MissionQuestion, QuestionVideo


class SkillSerializer(serializers.ModelSerializer):
    percent = serializers.SerializerMethodField()
    object = serializers.CharField(source="get_object_display")

    class Meta:
        model = StudentSkill
        fields = ("percent", "object")

    def get_percent(self, obj):
        return 100 * (obj.points / 12)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionVideo
        exclude = ("question", "id")


class StudentMissionSerializer(serializers.ModelSerializer):
    questions_count = serializers.IntegerField(source="mission.questions.count")

    class Meta:
        model = StudentMission
        exclude = ("student", "reaction", "answers")

    def update(self, instance, validated_data):
        instance.answers.update(validated_data.get("answers"))
        instance.reaction = validated_data.get("reaction", instance.reaction)
        instance.save()
        return instance


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MissionQuestion
        exclude = ("mission",)


class MissionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Mission
        exclude = ("coins",)
