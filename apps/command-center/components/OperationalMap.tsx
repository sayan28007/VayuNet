"use client";

import Script from "next/script";
import { useEffect, useMemo, useRef, useState } from "react";
import type { Hotspot } from "@/types/api";

interface Props {
  hotspots: Hotspot[] | null;
}

declare global {
  interface Window {
    google?: any;
  }
}

export default function OperationalMap({ hotspots }: Props) {
  const mapElement = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);
  const [mapsLoaded, setMapsLoaded] = useState(false);
  const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || "";

  const center = useMemo(() => {
    const first = hotspots?.[0];
    return first
      ? { lat: first.latitude, lng: first.longitude }
      : { lat: 20.5937, lng: 78.9629 };
  }, [hotspots]);

  useEffect(() => {
    if (!mapsLoaded || !window.google?.maps || !mapElement.current) return;

    if (!mapRef.current) {
      mapRef.current = new window.google.maps.Map(mapElement.current, {
        center,
        zoom: hotspots?.length ? 6 : 4,
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: false,
      });
    } else {
      mapRef.current.setCenter(center);
      mapRef.current.setZoom(hotspots?.length ? 6 : 4);
    }

    markersRef.current.forEach((marker) => marker.setMap(null));
    markersRef.current = (hotspots ?? []).map(
      (hotspot) =>
        new window.google.maps.Marker({
          position: { lat: hotspot.latitude, lng: hotspot.longitude },
          map: mapRef.current,
          title: `${hotspot.city ?? "Hotspot"} — VayuNet hotspot`,
        })
    );

    return () => {
      markersRef.current.forEach((marker) => marker.setMap(null));
      markersRef.current = [];
    };
  }, [mapsLoaded, center, hotspots]);

  if (!apiKey) {
    return (
      <section className="flex min-h-[320px] items-center justify-center rounded-2xl border border-dashed border-slate-700 bg-slate-900 p-6 text-center shadow-xl">
        <div>
          <div className="text-sm font-semibold text-slate-300">Operational Geospatial Map</div>
          <p className="mt-2 max-w-md text-xs leading-5 text-slate-500">
            Google Maps is not configured. Add NEXT_PUBLIC_GOOGLE_MAPS_API_KEY to enable the live hotspot map.
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 shadow-xl">
      <div className="border-b border-slate-800 p-4">
        <h2 className="text-lg font-bold text-white">Operational Map</h2>
        <p className="text-xs text-slate-400">Google Maps hotspot telemetry</p>
      </div>
      <Script
        src={`https://maps.googleapis.com/maps/api/js?key=${encodeURIComponent(apiKey)}&v=weekly`}
        strategy="afterInteractive"
        onLoad={() => setMapsLoaded(true)}
        onError={() => setMapsLoaded(false)}
      />
      <div ref={mapElement} className="min-h-[320px] w-full" />
    </section>
  );
}
