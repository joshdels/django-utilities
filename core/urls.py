from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("not-admin/", admin.site.urls),
    path("", include("api.urls")),
    path("jobs/", include("jobs.urls")),
    path("case-studies/", include("case_study.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
