from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Mission
from .serializers import MissionSerializer, QuestionSerializer


class MissionViewset(viewsets.GenericViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    @action(
        detail=True,
        url_name="questions",
        url_path="questions",
        serializer_class=QuestionSerializer
    )
    def questions(self, request, pk=None):
        mission = self.get_object()
        serialzier = self.serializer_class(mission.questions.all(), many=True)
        return Response(serialzier.data, status=status.HTTP_200_OK)
