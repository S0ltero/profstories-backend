from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Employer, Professional
from .serializers import (EmployerSerialzier, ProfessionalSerialzier,
                          EmployerCreateSerializer, ProfessionalCreateSerializer,
                          EmployerDetailSerializer, ProfessionalDetailSerializer)
# Create your views here.
