from django.urls import path, include
from api.views import (
    ProjectViewSet,
    AssetViewSet,
    NodeViewSet,
    LineViewSet,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"assets", AssetViewSet, basename="asset")
router.register(r"nodes", NodeViewSet, basename="node")
router.register(r"pipes", LineViewSet, basename="pipe")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
