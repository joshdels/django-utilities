from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)


class Asset(models.Model):
    ASSET_TYPE = [
        ("pipe", "Pipe"),
        ("value", "Valve"),
        ("hydrant", "Hydrant"),
        ("pump", "Pump"),
    ]

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, null=True, blank=True
    )
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE)
    name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, default="active")


class Node(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, null=True, blank=True)
    geometry = models.PointField(null=True, blank=True)


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
