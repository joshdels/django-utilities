from rest_framework import viewsets
from .models import CaseStudy, CaseStudyBlock
from .serializers import (
    CaseStudySerializer,
    CaseStudyListSerializer,
    CaseStudyBlockSerializer,
)

from core.permissions import IsAdminOrReadOnly


class CaseStudyViewSet(viewsets.ModelViewSet):
    queryset = CaseStudy.objects.all().order_by("-created_at")
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return CaseStudyListSerializer
        return CaseStudySerializer


class CaseStudyBlockViewSet(viewsets.ModelViewSet):
    queryset = CaseStudyBlock.objects.all().order_by("order")
    serializer_class = CaseStudyBlockSerializer
    permission_classes = [IsAdminOrReadOnly]
