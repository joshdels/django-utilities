from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=500, blank=True)
    utility_type = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to="logos/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"Project {self.id}"


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")
    name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to="project_files/")

    def __str__(self):
        return self.name or self.file.name


class Asset(models.Model):
    ASSET_TYPE = [
        ("pipe", "Pipe"),
        ("valve", "Valve"),
        ("hydrant", "Hydrant"),
        ("pump", "Pump"),
        ("tvalve", "T-Valve"),
    ]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, db_index=True, related_name="assets"
    )
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE)
    name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default="active")
    installed_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name or self.asset_type


class Node(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="node")
    geometry = models.PointField(null=True, blank=True, srid=4326)
    node_name = models.CharField(max_length=255, null=True, blank=True)
    node_type = models.CharField(max_length=100, null=True, blank=True)
    properties = models.JSONField(blank=True, null=True)
    elevation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.node_name or f"Node of {self.asset.name}"


class Line(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="line")
    start_node = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="outgoing_lines",
        null=True,
        blank=True,
    )
    end_node = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="incoming_lines",
        null=True,
        blank=True,
    )
    geometry = models.LineStringField(null=True, blank=True, srid=4326)
    line_name = models.CharField(max_length=255, null=True, blank=True)
    line_type = models.CharField(max_length=50, null=True, blank=True)
    material = models.CharField(max_length=50, blank=True)
    diameter = models.FloatField(null=True, blank=True)
    properties = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.line_name or f"Line of {self.asset.name}"
