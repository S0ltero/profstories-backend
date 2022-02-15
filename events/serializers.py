from rest_framework import serializers

from .models import Event


class EventSerialzier(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        exclude = ("employer",)
