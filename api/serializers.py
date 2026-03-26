from rest_framework import serializers
from .models import Project, ProjectFile, Asset, Node, Pipe


class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        files_data = request.FILES.getlist("files")

        logo = validated_data.get("logo", None)

        project = Project.objects.create(
            name=validated_data.get("name"),
            logo=logo,
            owner=request.user if request.user.is_authenticated else None,
        )

        for file in files_data:
            ProjectFile.objects.create(project=project, file=file)

        return project


class ProjectSerializer(serializers.ModelSerializer):
    files = ProjectFileSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ("owner",)


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
