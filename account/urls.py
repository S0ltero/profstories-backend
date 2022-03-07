from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"employers", EmployerViewset, basename="employers")
router.register(r"professionals", ProfessionalViewset, basename="professionals")
router.register(r"non-profit", NPOViewset, basename="non-profit")
router.register(r"colleges", CollegeViewset, basename="colleges")
router.register(r"agencies", EmploymentAgencyViewset, basename="agencies")
router.register(r"teachers", TeacherViewset, basename="teachers")

urlpatterns = [
] + router.urls
