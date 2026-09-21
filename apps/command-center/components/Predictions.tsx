"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { ExposureResponse, ForecastResponse, PlumeResponse } from "@/types/api";

interface Props { hotspotId: string; }

export default function Predictions({ hotspotId }: Props) {
  const [forecast, setForecast] = useState<ForecastResponse | null>(null);
  const [plume, setPlume] = useState<PlumeResponse | null>(null);
  const [exposure, setExposure] = useState<ExposureResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [partialError, setPartialError] = useState(false);

  useEffect(() => {
    if (!hotspotId) { setForecast(null); setPlume(null); setExposure(null); return; }
    let active = true;
    setLoading(true); setPartialError(false);
    Promise.allSettled([api.getForecast(hotspotId), api.getPlume(hotspotId), api.getExposure(hotspotId)]).then(([f, p, e]) => {
      if (!active) return;
      setForecast(f.status === "fulfilled" ? f.value : null);
      setPlume(p.status === "fulfilled" ? p.value : null);
      setExposure(e.status === "fulfilled" ? e.value : null);
      setPartialError([f, p, e].some((result) => result.status === "rejected"));
      setLoading(false);
    });
    return () => { active = false; };
  }, [hotspotId]);

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl">
      <h2 className="text-lg font-bold text-white">Predictions</h2><p className="mb-4 text-xs text-slate-400">Forecast, plume and population exposure</p>
      {loading && <div className="mb-3 text-xs text-slate-500">Refreshing prediction signals...</div>}
      {partialError && <div className="mb-3 text-xs text-amber-300">Some prediction signals are unavailable.</div>}
      <div className="space-y-4">
        <div className="rounded-xl bg-slate-950 p-4"><div className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-500">AQI Forecast</div><div className="space-y-2 text-sm text-slate-300">{(forecast?.forecasts ?? []).map((point) => <div key={point.horizon_minutes} className="flex justify-between"><span>{point.horizon_minutes} min</span><span>AQI: {Math.round(point.predicted_aqi)}</span></div>)}{!forecast && <span className="text-slate-500">Unavailable</span>}</div></div>
        <div className="rounded-xl bg-slate-950 p-4"><div className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-500">Plume</div><div className="space-y-2 text-sm text-slate-300">{(plume?.horizons ?? []).slice(-3).map((h) => <div key={h.minutes} className="flex justify-between"><span>{h.minutes} min</span><span>{h.radius_km.toFixed(1)} km</span></div>)}{!plume && <span className="text-slate-500">Unavailable</span>}</div></div>
        <div className="rounded-xl bg-slate-950 p-4"><div className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-500">Exposure</div>{exposure ? <div className="grid grid-cols-2 gap-3 text-sm text-slate-300"><div><span className="block text-xs text-slate-500">Population</span>{exposure.estimated_population.toLocaleString()}</div><div><span className="block text-xs text-slate-500">Area</span>{exposure.area_km2.toFixed(1)} km²</div></div> : <span className="text-sm text-slate-500">Unavailable</span>}</div>
      </div>
    </section>
  );
}
