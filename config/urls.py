from django.contrib import admin
from django.urls import path, include

from account.views import CallbackCreateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("account.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("api/", include("events.urls")),
    path("api/callback/", CallbackCreateView.as_view())
]
