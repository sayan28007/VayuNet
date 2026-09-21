"use client";

import type { Hotspot } from "@/types/api";

interface Props {
  hotspots: Hotspot[] | null;
  loading: boolean;
  error: string | null;
  selectedHotspotId: string;
  onSelectHotspot: (id: string) => void;
}

export default function Hotspots({ hotspots, loading, error, selectedHotspotId, onSelectHotspot }: Props) {
  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-white">Detected Hotspots</h2>
          <p className="text-xs text-slate-400">Multimodal evidence fusion output</p>
        </div>
        <span className="rounded-full bg-cyan-500/10 px-2.5 py-1 text-xs font-semibold text-cyan-300">
          {hotspots?.length ?? 0} active
        </span>
      </div>

      {loading && <div className="text-sm text-slate-400">Loading hotspots...</div>}
      {!loading && error && <div className="text-sm text-amber-300">Unavailable</div>}
      {!loading && !error && (hotspots?.length ?? 0) === 0 && (
        <div className="text-sm text-slate-500">No hotspots detected.</div>
      )}

      <div className="space-y-3">
        {(hotspots ?? []).map((hotspot) => {
          const active = hotspot.hotspot_id === selectedHotspotId;
          return (
            <button
              key={hotspot.hotspot_id}
              type="button"
              onClick={() => onSelectHotspot(hotspot.hotspot_id)}
              className={`w-full rounded-xl border p-4 text-left transition ${
                active ? "border-cyan-500/60 bg-cyan-500/5" : "border-slate-800 bg-slate-950 hover:border-slate-700"
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="font-semibold text-white">ID: {hotspot.hotspot_id}</div>
                  <div className="mt-1 text-xs text-slate-400">
                    City: {hotspot.city ?? "Unknown"} · Severity: {hotspot.severity}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-cyan-300">Score: {Math.round(hotspot.score)}</div>
                  <div className="text-xs text-slate-500">Confidence {(hotspot.confidence * 100).toFixed(0)}%</div>
                </div>
              </div>
              <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-300 md:grid-cols-4">
                <span>Evidence {hotspot.evidence_count}</span>
                <span>Anomaly {hotspot.anomaly_score.toFixed(1)}</span>
                <span>Spatial {hotspot.spatial_score.toFixed(1)}</span>
                <span>Quality {(hotspot.data_quality_score * 100).toFixed(0)}%</span>
              </div>
              <div className="mt-3 text-xs text-slate-400">{hotspot.explanation}</div>
            </button>
          );
        })}
      </div>
    </section>
  );
}
