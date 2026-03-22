from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Asset, Node, Pipe
from .serializers import *


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(owner=user)


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


class PipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PipeSerializer

    def get_queryset(self):
        user = self.request.user
        return Pipe.objects.filter(asset__project__owner=user)
