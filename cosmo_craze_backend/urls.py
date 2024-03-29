from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda request: HttpResponse("Welcome to Cosmo Craze Backend")),
    path("auth/", include("userauths.urls")),
    path("core/", include("core.urls")),
]
