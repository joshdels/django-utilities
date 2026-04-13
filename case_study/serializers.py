from rest_framework import serializers
from .models import CaseStudy, CaseStudyBlock


class CaseStudyBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyBlock
        fields = "__all__"


class CaseStudyListSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = CaseStudy
        fields = [
            "id",
            "title",
            "description",
            "image",
            "is_highlight",
            "tags",
            "created_at",
        ]


class CaseStudySerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    blocks = CaseStudyBlockSerializer(many=True, read_only=True)

    class Meta:
        model = CaseStudy
        fields = [
            "id",
            "title",
            "description",
            "image",
            "tags",
            "created_at",
            "blocks",
        ]
