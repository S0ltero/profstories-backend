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


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    video = VideoSerializer(source="videos.first")

    class Meta:
        model = MissionQuestion
        exclude = ("mission",)

    def get_answers(self, obj):
        return obj.answers.keys()


class StudentMissionSerializer(serializers.ModelSerializer):
    questions_count = serializers.IntegerField(source="mission.questions.count")

    class Meta:
        model = StudentMission
        exclude = ("student", "reaction", "answers")


class StudentMissionCreateSerializer(serializers.ModelSerializer):
    questions_count = serializers.IntegerField(source="mission.questions.count")

    class Meta:
        model = StudentMission
        exclude = ("student",)

    def update(self, instance, validated_data):
        if validated_data.get("answers"):
            instance.answers.update(validated_data.pop("answers"))
        if validated_data.get("reaction"):
            instance.reaction = validated_data.pop("reaction")
        if validated_data.get("is_complete"):
            instance.is_complete = validated_data.pop("is_complete")
        instance.save()
        return instance


class MissionSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Mission
        exclude = ("coins",)
