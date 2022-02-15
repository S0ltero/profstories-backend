from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Employer, Professional
from .serializers import (EmployerSerialzier, ProfessionalSerialzier,
                          EmployerCreateSerializer, ProfessionalCreateSerializer,
                          EmployerDetailSerializer, ProfessionalDetailSerializer)


class EmployerViewset(viewsets.GenericViewSet):
    queryset = Employer
    serializer_class = EmployerSerialzier
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return EmployerCreateSerializer
        else:
            return EmployerSerialzier

    def retrieve(self, request, pk):
        try:
            employer = self.queryset.objects.get(user_id=pk)
        except Employer.DoesNotExist:
            return Response(f"Работодатель {pk} не найден", status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(employer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if serializer.is_valid(raise_exception=False):
            serializer.save(user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            employer = self.queryset.objects.get(user_id=pk)
        except Employer.DoesNotExist:
            return Response(f"Работодатель {pk} не найден", status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer_class()
        serializer = serializer(employer, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(employer, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            employers = self.queryset.objects.all()
            page = self.paginate_queryset(employers)
        except Employer.DoesNotExist:
            return Response("Работодатели не найдены", status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, url_path='detail', url_name='detail', serializer_class=EmployerDetailSerializer)
    def qdetail(self, request, pk=None):
        try:
            employer = self.queryset.objects.get(user_id=pk)
        except Employer.DoesNotExist:
            return Response(f"Работодатель {pk} не найден", status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(employer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfessionalViewset(viewsets.GenericViewSet):
    queryset = Professional
    serializer_class = ProfessionalSerialzier
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return ProfessionalCreateSerializer
        else:
            return ProfessionalSerialzier

    def retrieve(self, request, pk):
        try:
            professional = self.queryset.objects.get(user_id=pk)
        except Employer.DoesNotExist:
            return Response(f"Работодатель {pk} не найден", status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(professional)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = self.get_serializer_class()
        serializer = serializer(data=data)
        if serializer.is_valid(raise_exception=False):
            serializer.save(user_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            professional = self.queryset.objects.get(user_id=pk)
        except Professional.DoesNotExist:
            return Response(f"Профессионал {pk} не найден", status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer_class()
        serializer = serializer(professional, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=False):
            serializer.update(professional, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            professionals = self.queryset.objects.all()
            page = self.paginate_queryset(professionals)
        except Professional.DoesNotExist:
            return Response("Профессионалы не найдены", status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, url_path='detail', url_name='detail', serializer_class=ProfessionalDetailSerializer)
    def qdetail(self, request, pk=None):
        try:
            professional = self.queryset.objects.get(user_id=pk)
        except Professional.DoesNotExist:
            return Response(f"Профессионал {pk} не найден", status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(professional)
        return Response(serializer.data, status=status.HTTP_200_OK)
