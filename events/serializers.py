from rest_framework import serializers

from .models import Event


class EventSerialzier(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        exclude = ("employer",)


class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"


class EventDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = "__all__"