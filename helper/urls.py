from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"missions", MissionViewset, basename="missions")

urlpatterns = [
] + router.urls
