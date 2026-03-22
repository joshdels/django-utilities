"use client";

import { useRef, useEffect, useState } from "react";
import maplibregl, { Map } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import styles from "./Map.module.css";

export default function DemoMap() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<Map | null>(null);

  const [lng] = useState(-74.5);
  const [lat] = useState(40);
  const [zoom] = useState(9);

  useEffect(() => {
    if (map.current) return;
    if (!mapContainer.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style:
        "https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json",
      center: [lng, lat],
      zoom: zoom,
      attributionControl: false,
    });

    map.current.addControl(new maplibregl.NavigationControl(), "top-right");

    // map.current.on("load", async () => {
    //   try {
    //     const geojsonUrl = "/sample_web.geojson";

    //     const res = await fetch(geojsonUrl);
    //     const data = await res.json();

    //     map.current?.addSource("layer-data", {
    //       type: "geojson",
    //       data: data,
    //     });

    //     map.current?.addLayer({
    //       id: "my-data-layer",
    //       type: "line",
    //       source: "layer-data",
    //       minzoom: 12,
    //       paint: {
    //         "line-color": "orange",
    //         "line-width": 2,
    //       },
    //     });

    //     const bounds = new maplibregl.LngLatBounds();

    //     data.features.forEach((feature: any) => {
    //       const geom = feature.geometry;
    //       if (!geom) return;

    //       const addCoords = (coords: any) => {
    //         if (
    //           Array.isArray(coords) &&
    //           typeof coords[0] === "number" &&
    //           typeof coords[1] === "number"
    //         ) {
    //           bounds.extend(coords);
    //         } else if (Array.isArray(coords)) {
    //           coords.forEach(addCoords);
    //         }
    //       };

    //       addCoords(geom.coordinates);
    //     });

    //     if (!bounds.isEmpty()) {
    //       map.current?.fitBounds(bounds, {
    //         padding: 50,
    //         duration: 1000,
    //       });
    //     } else {
    //       console.warn("Bounds empty — check GeoJSON");
    //     }
    //   } catch (err) {
    //     console.error("GeoJSON error:", err);
    //   }
    // });

    return () => {
      map.current?.remove();
      map.current = null;
    };
  }, [lng, lat, zoom]);

  return <div className={styles["map-container"]} ref={mapContainer} />;
}
