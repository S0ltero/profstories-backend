from distutils.util import strtobool

from django.utils import timezone
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event
from .serializers import EventSerialzier, EventDetailSerializer, EventCreateSerializer


class EventViewset(viewsets.GenericViewSet):
    queryset = Event
    serializer_class = EventSerialzier

    def get_queryset(self):
        queryset = Event.objects.filter(verification=Event.Verifiaction.VERIFIED)

        mode = self.request.query_params.get("mode")
        if mode:
            queryset = queryset.filter(mode=mode)

        terms = self.request.query_params.get("terms")
        if terms:
            terms = list(map(strtobool, terms.split(",")))
            queryset = queryset.filter(is_free__in=terms)

        status = self.request.query_params.get("status")
        if status:
            status = strtobool(status)
            if status:
                queryset = queryset.filter(date__gte=timezone.now())
            elif not status:
                queryset = queryset.filter(date__lt=timezone.now())

        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(date__date=date)

        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EventCreateSerializer
        else:
            return EventSerialzier

    def retrieve(self, request, pk):
        try:
            event = self.queryset.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(f"Мероприятие {pk} не найдено", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=False):
            serializer.save(user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        pk = request.data["id"]
        try:
            event = self.queryset.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(f"Мероприятие {pk} не найдено", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(event, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(event, serializer.validated_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            events = self.get_queryset()
        except Event.DoesNotExist:
            return Response("Мероприятия не найдены", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, url_path='detail', url_name='detail', serializer_class=EventDetailSerializer)
    def qdetail(self, request, pk=None):
        try:
            event = self.queryset.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(f"Мероприятие {pk} не найдено", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
