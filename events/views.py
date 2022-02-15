from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Event
from .serializers import EventSerialzier, EventDetailSerializer, EventCreateSerializer

# Create your views here.
