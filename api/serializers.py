from rest_framework import serializers
from .models import Project, Asset, Node, Pipe


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = "__all__"


class PipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipe
        fields = "__all__"
