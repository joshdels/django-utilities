from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=500, blank=True)
    logo = models.ImageField(upload_to="logos/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectFile(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to="project_files/")


class Asset(models.Model):
    UTILITY_TYPE = [
        ("water", "Water"),
        ("electricity", "Electricity"),
        ("irrigation", "Irrigation"),
        ("sewerage", "Sewerage"),
    ]

    ASSET_TYPE = [
        ("pipe", "Pipe"),
        ("valve", "Valve"),
        ("hydrant", "Hydrant"),
        ("pump", "Pump"),
        ("tvalve", "T-Valve"),
    ]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True
    )
    utility_type = models.CharField(max_length=20, choices=UTILITY_TYPE)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE)
    name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default="active")
    properties = models.JSONField(blank=True, null=True)


class Node(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="node")
    geometry = models.PointField(null=True, blank=True)
    properties = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Node: {self.asset.name if self.asset else 'Unnamed'}"


class Pipe(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)
    start_node = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="start_pipes",
        null=True,
        blank=True,
    )
    end_node = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="end_pipes", null=True, blank=True
    )
    geometry = models.LineStringField(null=True, blank=True)
    diameter = models.FloatField(null=True, blank=True)
    material = models.CharField(max_length=50, blank=True)
    properties = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Pipe: {self.asset.name if self.asset else 'Unnamed'}"
