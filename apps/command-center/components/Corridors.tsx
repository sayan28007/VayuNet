"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { CorridorPrediction } from "@/types/api";

export default function Corridors() {
  const [corridors, setCorridors] = useState<CorridorPrediction[]>([]);
  const [error, setError] = useState(false);

  useEffect(() => {
    api.getCorridorPredictions().then(setCorridors).catch(() => setError(true));
  }, []);

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl">
      <h2 className="text-lg font-bold text-white">Corridor Risk</h2>
      <p className="mb-4 text-xs text-slate-400">Predicted AQI along monitored corridors</p>
      {error && <div className="text-sm text-amber-300">Unavailable</div>}
      <div className="space-y-3">
        {corridors.map((c) => (
          <div key={c.corridor_name} className="rounded-xl bg-slate-950 p-4">
            <div className="flex justify-between gap-3"><span className="font-semibold text-white">{c.corridor_name}</span><span className="text-xs font-semibold text-amber-300">{c.risk_level}</span></div>
            <div className="mt-2 grid grid-cols-2 gap-2 text-xs text-slate-300 md:grid-cols-4">
              <span>Current AQI: {c.current_aqi}</span>
              <span>1h: {c.predicted_aqi_1h}</span>
              <span>2h: {c.predicted_aqi_2h}</span>
              <span>3h: {c.predicted_aqi_3h}</span>
            </div>
            <div className="mt-2 text-xs text-slate-500">Peak {c.predicted_peak_aqi} · {c.time_to_peak_minutes} min</div>
          </div>
        ))}
        {!error && corridors.length === 0 && <div className="text-sm text-slate-500">No corridor data.</div>}
      </div>
    </section>
  );
}
