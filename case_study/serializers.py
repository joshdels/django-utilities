from rest_framework import serializers
from .models import CaseStudy, CaseStudyBlock


class CaseStudyBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyBlock
        fields = "__all__"


class CaseStudyListSerializer(serializers.ModelSerializer):
    money_tag = serializers.StringRelatedField()

    class Meta:
        model = CaseStudy
        fields = [
            "id",
            "title",
            "main_image",
            "money_tag",
            "created_at",
        ]


class CaseStudySerializer(serializers.ModelSerializer):
    money_tag = serializers.StringRelatedField()
    blocks = CaseStudyBlockSerializer(many=True, read_only=True)

    class Meta:
        model = CaseStudy
        fields = [
            "id",
            "title",
            "description",
            "main_image",
            "money_tag",
            "created_at",
            "blocks",
        ]
