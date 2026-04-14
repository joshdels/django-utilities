import ezdxf
import geopandas as gpd
import pathlib
import logging
from shapely.geometry import Point, LineString, Polygon
from typing import Optional

logger = logging.getLogger(__name__)


def parse_entity(entity) -> Optional[object]:
    etype = entity.dxftype()

    try:
        if etype in ["POINT", "INSERT"]:
            coords = entity.dxf.insert if etype == "INSERT" else entity.dxf.location
            return Point(coords.x, coords.y)

        elif etype == "LINE":
            return LineString(
                [
                    (entity.dxf.start.x, entity.dxf.start.y),
                    (entity.dxf.end.x, entity.dxf.end.y),
                ]
            )

        elif etype == "LWPOLYLINE":
            points = [(p[0], p[1]) for p in entity.get_points()]
            if entity.closed and len(points) >= 3:
                return Polygon(points)
            elif len(points) > 1:
                return LineString(points)

        elif etype == "HATCH":
            try:
                for path in entity.paths:
                    if hasattr(path, "vertices"):
                        points = [(pt[0], pt[1]) for pt in path.vertices]
                        if len(points) >= 3:
                            return Polygon(points)
            except Exception:
                return None

        return None

    except Exception:
        return None


def dxf_to_dataframe(doc) -> gpd.GeoDataFrame:
    msp = doc.modelspace()
    rows = []

    for entity in msp:
        geom = parse_entity(entity)
        if geom:
            rows.append(
                {
                    "geometry": geom,
                    "layer": entity.dxf.layer,
                    "cad_type": entity.dxftype().upper(),
                }
            )

    return gpd.GeoDataFrame(rows, geometry="geometry")


def extract_to_geopackage(
    file_path: str,
    output_path: str,
    crs: str = None,
):
    logger.info("Extracting DXF to GeoPackage...")

    input_path = pathlib.Path(file_path)

    if not input_path.exists() or input_path.suffix.lower() != ".dxf":
        raise FileNotFoundError(f"Invalid DXF file: {file_path}")

    try:
        doc = ezdxf.readfile(file_path)

        msp = doc.modelspace()
        geodata = msp.get_geodata()
        dxf_crs = None

        if geodata:
            try:
                code, _ = geodata.get_crs()
                if code:
                    dxf_crs = f"EPSG:{code}"
            except Exception:
                dxf_crs = None

        gdf = dxf_to_dataframe(doc)

        if gdf.empty:
            raise ValueError("No valid geometry found in DXF")

        final_crs = dxf_crs or crs

        if final_crs:
            if gdf.crs is None:
                gdf = gdf.set_crs(final_crs)
            elif gdf.crs != final_crs:
                logger.warning(f"CRS mismatch: {gdf.crs} vs {final_crs}")

        out_path = pathlib.Path(output_path)
        gdf.to_file(out_path, layer="entities", driver="GPKG")

        logger.info(f"Exported to {out_path.resolve()}")

        return out_path

    except Exception as e:
        logger.exception("DXF conversion failed")
        raise RuntimeError(f"DXF conversion failed: {e}")
