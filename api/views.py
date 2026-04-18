from django.contrib.gis.geos import GEOSGeometry
import geopandas as gpd
import pandas as pd
import uuid
import json
import os

from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django.db import transaction

from .serializers import (
    ProjectSerializer,
)


from .models import (
    Project,
    DatasetVersion,
    Asset,
    Layer,
    Node,
    Line,
    Area,
)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UploadStatusView(APIView):

    def get(self, request, project_id):

        project = get_object_or_404(Project, id=project_id)

        versions = DatasetVersion.objects.filter(project=project)

        return Response(
            {
                "project": project.id,
                "versions": [
                    {
                        "version": v.version,
                        "is_active": v.is_active,
                        "asset_count": Asset.objects.filter(version=v).count(),
                    }
                    for v in versions
                ],
            }
        )


class UploadDatasetView(APIView):
    """
    POST:
    - project_id (int)
    - file (GeoJSON)
    """

    @transaction.atomic
    def post(self, request):

        file = request.FILES.get("file")

        file_name = os.path.splitext(file.name)[0]
        project_id = request.data.get("project_id")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        if not project_id:
            return Response({"error": "project_id is required"}, status=400)

        # =========================
        # PROJECT
        # =========================
        project = get_object_or_404(Project, id=project_id)

        # =========================
        # VERSIONING
        # =========================
        last_version = (
            DatasetVersion.objects.filter(project=project).order_by("-version").first()
        )

        next_version = (last_version.version + 1) if last_version else 1

        version = DatasetVersion.objects.create(
            project=project,
            version=next_version,
            created_by=request.user,
            is_active=True,
        )

        DatasetVersion.objects.filter(project=project).exclude(id=version.id).update(
            is_active=False
        )

        project.current_version = version
        project.save()

        # =========================
        # READ GEOJSON
        # =========================
        try:
            gdf = gpd.read_file(file)
        except Exception as e:
            return Response(
                {"error": "Invalid GeoJSON", "details": str(e)},
                status=400,
            )

        created_assets = 0

        # =========================
        # PROCESS FEATURES
        # =========================
        for _, row in gdf.iterrows():

            geom = row.geometry

            if geom is None or geom.is_empty:
                continue

            # =========================
            # NORMALIZE GEOMETRY TYPE
            # =========================
            geom_type = geom.geom_type

            if geom_type.startswith("Multi"):
                geom_type = geom_type.replace("Multi", "")

            geoms = list(geom.geoms) if hasattr(geom, "geoms") else [geom]

            # =========================
            # AUTO-CREATE / GET LAYER
            # =========================
            layer, created = Layer.objects.get_or_create(
                project=project,
                geometry_type=geom_type,
                defaults={
                    "name": file_name,
                    "is_active": True,
                    "schema": {},
                },
            )

            # =========================
            # CLEAN PROPERTIES
            # =========================
            properties = {
                k: (None if pd.isna(v) else v)
                for k, v in row.items()
                if k != "geometry"
            }

            # =========================
            # CREATE ASSET
            # =========================
            asset = Asset.objects.create(
                project=project,
                version=version,
                layer=layer,
                global_id=uuid.uuid4(),
                external_id=str(row.get("id", uuid.uuid4())),
                name=str(row.get("name", "")),
                status=str(row.get("status", "active")),
            )

            # =========================
            # SAVE GEOMETRY
            # =========================
            for g in geoms:

                django_geom = GEOSGeometry(g.wkt, srid=4326)

                if geom_type == "Point":
                    Node.objects.create(
                        asset=asset,
                        geometry=django_geom,
                        properties=properties,
                    )

                elif geom_type == "LineString":
                    Line.objects.create(
                        asset=asset,
                        geometry=django_geom,
                        properties=properties,
                    )

                elif geom_type == "Polygon":
                    Area.objects.create(
                        asset=asset,
                        geometry=django_geom,
                        name=str(row.get("name", "")),
                        properties=properties,
                    )

            created_assets += 1

        return Response(
            {
                "message": "Upload successful",
                "project": project.id,
                "version": version.version,
                "assets_created": created_assets,
            },
            status=status.HTTP_201_CREATED,
        )


class ProjectFeaturesView(APIView):

    def get(self, request, project_id):

        # =========================
        # PROJECT
        # =========================
        project = get_object_or_404(Project, id=project_id)

        # =========================
        # VERSION (OPTIONAL)
        # =========================
        version_id = request.query_params.get("version")

        if version_id:
            version = get_object_or_404(DatasetVersion, id=version_id, project=project)
        else:
            version = project.current_version

        if not version:
            return Response({"error": "No active version found"}, status=400)

        # =========================
        # OPTIONAL FILTERS
        # =========================
        active_only = request.query_params.get("active", "false").lower() == "true"
        layer_name = request.query_params.get("layer")

        base_filter = {
            "asset__project": project,
        }

        # ONLY lock version if explicitly requested (ArcGIS-style)
        if version_id:
            base_filter["asset__version"] = version

        if active_only:
            base_filter["asset__layer__is_active"] = True

        if layer_name:
            base_filter["asset__layer__name"] = layer_name

        # =========================
        # QUERY HELPERS
        # =========================
        def build_node(n):
            return {
                "type": "Feature",
                "id": n.asset.external_id,
                "geometry": n.geometry.geojson if n.geometry else None,
                "properties": n.properties,
                "elevation": n.elevation,
            }

        def build_line(l):
            return {
                "type": "Feature",
                "id": l.asset.external_id,
                "geometry": l.geometry.geojson if l.geometry else None,
                "start_node": l.start_node.asset.external_id if l.start_node else None,
                "end_node": l.end_node.asset.external_id if l.end_node else None,
                "properties": l.properties,
            }

        def build_area(a):
            return {
                "type": "Feature",
                "id": a.asset.external_id,
                "geometry": a.geometry.geojson if a.geometry else None,
                "area_type": a.area_type,
                "properties": a.properties,
            }

        # =========================
        # QUERIES
        # =========================
        nodes = Node.objects.filter(**base_filter)
        lines = Line.objects.filter(**base_filter)
        areas = Area.objects.filter(**base_filter)

        # =========================
        # RESPONSE (ArcGIS-style FeatureSet)
        # =========================
        return Response(
            {
                "type": "FeatureCollection",
                "project": project.id,
                "version": version.version if version else None,
                "query": {
                    "version_locked": version_id is not None,
                    "active": active_only,
                    "layer": layer_name,
                },
                "features": {
                    "nodes": [build_node(n) for n in nodes],
                    "lines": [build_line(l) for l in lines],
                    "areas": [build_area(a) for a in areas],
                },
            }
        )
