from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("not-admin/", admin.site.urls),
    path("", include("api.urls")),
]
