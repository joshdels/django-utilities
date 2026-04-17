from django.urls import path, include
from api.views import (
    ProjectViewSet,
    UploadDatasetView,
    UploadStatusView,
    ProjectFeaturesView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    path("upload/status/<int:project_id>/", UploadStatusView.as_view()),
    path("upload/dataset/", UploadDatasetView.as_view(), name="upload-dataset"),
    path("project/<int:project_id>/features/", ProjectFeaturesView.as_view()),
]
