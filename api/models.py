import uuid
from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=500, blank=True)
    logo = models.ImageField(upload_to="logos/", null=True, blank=True)

    current_version = models.ForeignKey(
        "DatasetVersion",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"Project {self.id}"


class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")
    name = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(upload_to="project_files/")

    def __str__(self):
        return self.name or self.file.name


class DatasetVersion(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    version = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "version")
        ordering = ["-version"]

    def __str__(self):
        return f"{self.project.name} v{self.version}"


class Layer(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="layers"
    )

    dataset_version = models.ForeignKey(
        DatasetVersion, on_delete=models.SET_NULL, null=True, blank=True
    )

    name = models.CharField(max_length=100)
    geometry_type = models.CharField(
        max_length=50,
        choices=[
            ("Point", "Point"),
            ("LineString", "LineString"),
            ("Polygon", "Polygon"),
        ],
    )

    is_active = models.BooleanField(default=True)

    schema = models.JSONField(default=dict)

    class Meta:
        unique_together = ("project", "name", "dataset_version")

    def __str__(self):
        return f"{self.name} ({self.project.name})"


class Asset(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    version = models.ForeignKey(
        DatasetVersion, on_delete=models.CASCADE, null=True, blank=True
    )

    global_id = models.UUIDField(
        default=uuid.uuid4, editable=False, null=True, blank=True
    )
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE)

    external_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default="active")

    class Meta:
        indexes = [
            models.Index(fields=["project", "version"]),
            models.Index(fields=["external_id"]),
            models.Index(fields=["layer"]),
        ]

    def __str__(self):
        return self.name or self.external_id


class Node(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="node")
    geometry = models.PointField(null=True, blank=True, srid=4326)
    properties = models.JSONField(default=dict, blank=True, null=True)

    elevation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.asset.name or f"Node {self.asset.external_id}"


class Line(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="line")
    start_node = models.ForeignKey(
        Node,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="outgoing_lines",
    )
    end_node = models.ForeignKey(
        Node,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="incoming_lines",
    )
    geometry = models.LineStringField(null=True, blank=True, srid=4326)
    properties = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.asset.name or f"Line {self.asset.external_id}"


class Area(models.Model):
    asset = models.OneToOneField("Asset", on_delete=models.CASCADE, related_name="area")

    geometry = models.PolygonField(srid=4326)

    name = models.CharField(max_length=255, blank=True)
    area_type = models.CharField(max_length=100, blank=True)

    properties = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name or f"Area of {self.asset.external_id}"
