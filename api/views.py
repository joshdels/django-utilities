from django.contrib.gis.geos import GEOSGeometry
import geopandas as gpd
import pandas as pd
import uuid

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
    AssetType,
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


class UploadDatasetView(APIView):
    """
    POST:
    - project_id (int)
    - file (GeoJSON)
    """

    @transaction.atomic
    def post(self, request):
        file = request.FILES.get("file")
        project_id = request.data.get("project_id")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        if not project_id:
            return Response({"error": "project_id is required"}, status=400)

        # =========================
        # GET PROJECT
        # =========================
        project = get_object_or_404(Project, id=project_id)

        # =========================
        # CREATE VERSION
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
                {"error": "Invalid GeoJSON / file format", "details": str(e)},
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

            geom_type = geom.geom_type

            # =========================
            # FLATTEN MULTI-GEOMETRIES
            # =========================
            if geom_type == "MultiPoint":
                geoms = list(geom.geoms)
                geom_type = "Point"

            elif geom_type == "MultiLineString":
                geoms = list(geom.geoms)
                geom_type = "LineString"

            elif geom_type == "MultiPolygon":
                geoms = list(geom.geoms)
                geom_type = "Polygon"

            else:
                geoms = [geom]

            # =========================
            # MATCH ASSET TYPE
            # =========================
            asset_type = AssetType.objects.filter(
                project=project, geometry_type=geom_type
            ).first()

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
                asset_type=asset_type,
                global_id=uuid.uuid4(),
                external_id=str(row.get("id", uuid.uuid4())),
                name=str(row.get("name", "")),
                status=str(row.get("status", "active")),
            )

            # =========================
            # SAVE GEOMETRIES (IMPORTANT FIX HERE)
            # =========================
            for g in geoms:

                # 🔥 CRITICAL FIX: convert Shapely → GEOSGeometry
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

        # SAFE FETCH
        project = get_object_or_404(Project, id=project_id)
        version = project.current_version

        if not version:
            return Response({"error": "No active version found"}, status=400)

        # =========================
        # NODES
        # =========================
        nodes = Node.objects.filter(asset__project=project, asset__version=version)

        node_data = [
            {
                "id": n.asset.external_id,
                "name": n.asset.name,
                "geometry": n.geometry.geojson if n.geometry else None,
                "properties": n.properties,
                "elevation": n.elevation,
            }
            for n in nodes
        ]

        # =========================
        # LINES
        # =========================
        lines = Line.objects.filter(asset__project=project, asset__version=version)

        line_data = [
            {
                "id": l.asset.external_id,
                "name": l.asset.name,
                "geometry": l.geometry.geojson if l.geometry else None,
                "start_node": l.start_node.asset.external_id if l.start_node else None,
                "end_node": l.end_node.asset.external_id if l.end_node else None,
                "properties": l.properties,
            }
            for l in lines
        ]

        # =========================
        # AREAS
        # =========================
        areas = Area.objects.filter(asset__project=project, asset__version=version)

        area_data = [
            {
                "id": a.asset.external_id,
                "name": a.name,
                "geometry": a.geometry.geojson if a.geometry else None,
                "area_type": a.area_type,
                "properties": a.properties,
            }
            for a in areas
        ]

        return Response(
            {
                "project": project.id,
                "version": version.version,
                "nodes": node_data,
                "lines": line_data,
                "areas": area_data,
            }
        )


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
