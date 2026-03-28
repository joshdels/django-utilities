from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, ProjectFile, Asset, Node, Line
from .serializers import (
    ProjectSerializer,
    AssetSerializer,
    NodeSerializer,
    LineSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AssetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AssetSerializer

    def get_queryset(self):
        user = self.request.user
        return Asset.objects.filter(project__owner=user)


class NodeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NodeSerializer

    def get_queryset(self):
        user = self.request.user
        return Node.objects.filter(asset__project__owner=user)


class LineViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LineSerializer

    def get_queryset(self):
        user = self.request.user
        return Line.objects.filter(asset__project__owner=user)
