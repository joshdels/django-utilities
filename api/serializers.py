from rest_framework import serializers
from .models import Project, ProjectFile, Asset, Node, Line


class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = "__all__"
        read_only_fields = ["id"]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["id", "created_at", "owner"]

    def create(self, validated_data):
        request = self.context.get("request")
        project = Project.objects.create(
            name=validated_data.get("name", ""),
            description=validated_data.get("description", ""),
            logo=validated_data.get("logo", None),
            owner=request.user if request.user.is_authenticated else None,
        )
        files_data = request.FILES.getlist("file")
        for file in files_data:
            ProjectFile.objects.create(project=project, file=file, name=file.name)

        return project

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        if validated_data.get("logo") is not None:
            instance.logo = validated_data.get("logo")
        instance.save()
        return instance
