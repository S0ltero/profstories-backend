from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"employers", EmployerViewset, basename="employers")
router.register(r"professionals", ProfessionalViewset, basename="professionals")

urlpatterns = [
] + router.urls