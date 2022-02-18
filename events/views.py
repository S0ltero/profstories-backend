from distutils.util import strtobool

from django.utils import timezone
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Event
from .serializers import EventSerialzier, EventDetailSerializer, EventCreateSerializer


class EventViewset(viewsets.GenericViewSet):
    queryset = Event
    serializer_class = EventSerialzier
    pagination_class = PageNumberPagination

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
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save(employer_id=request.user.id)
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
            employers = self.get_queryset()
            page = self.paginate_queryset(employers)
        except Event.DoesNotExist:
            return Response("Мероприятия не найдены", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, url_path='detail', url_name='detail', serializer_class=EventDetailSerializer)
    def qdetail(self, request, pk=None):
        try:
            event = self.queryset.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response(f"Мероприятие {pk} не найдено", status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
