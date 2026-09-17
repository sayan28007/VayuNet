"use client";
import React, { useEffect, useState } from "react";
import api from "../lib/api";
import { DashboardMetrics } from "../components/DashboardMetrics";
import { ObservationList } from "../components/ObservationList";
import { HotspotList } from "../components/HotspotList";
import { PredictionPanel } from "../components/PredictionPanel";
import { CorridorPanel } from "../components/CorridorPanel";
import { ExposurePanel } from "../components/ExposurePanel";
import AICommandCenter from "../components/AICommandCenter";
import AuthorityResponse from "../components/AuthorityResponse";
import FederatedLearningPanel from "../components/FederatedLearningPanel";

export default function CommandCenterPage() {
  const [apiStatus, setApiStatus] = useState<string>("Connecting...");
  const [observations, setObservations] = useState<any[]>([]);
  const [hotspots, setHotspots] = useState<any[]>([]);
  const [corridors, setCorridors] = useState<any[]>([]);
  const [selectedHotspotId, setSelectedHotspotId] = useState<string | null>(null);
  const [forecast, setForecast] = useState<any>(null);
  const [plume, setPlume] = useState<any>(null);
  const [exposure, setExposure] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const health = await api.getHealth();
        setApiStatus(health.status ? `Connected (${health.status})` : "Active");

        const obsData = await api.getObservations();
        setObservations(obsData || []);

        const hotspotData = await api.getHotspots();
        setHotspots(hotspotData || []);
        if (hotspotData && hotspotData.length > 0) {
          setSelectedHotspotId(hotspotData[0].hotspot_id);
        }

        const corridorData = await api.getCorridors();
        setCorridors(corridorData || []);
      } catch (err) {
        setApiStatus("Backend Offline");
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  useEffect(() => {
    if (!selectedHotspotId) return;
    api.getForecast(selectedHotspotId).then(setForecast).catch(() => setForecast(null));
    api.getPlume(selectedHotspotId).then(setPlume).catch(() => setPlume(null));
    api.getExposure(selectedHotspotId).then(setExposure).catch(() => setExposure(null));
  }, [selectedHotspotId]);

  return (
    <main className="min-h-screen bg-slate-950 text-white p-6 md:p-10 space-y-8">
      <header className="border-b border-slate-800 pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-black tracking-tight text-cyan-400">VayuNet Command Center</h1>
          <p className="text-xs text-slate-400">Phase 1–6: Telemetry, Predictions, Authority Response & Federated Learning</p>
        </div>
        <div className="text-xs bg-slate-900 border border-slate-800 px-3 py-1.5 rounded text-slate-300">
          Status: {apiStatus}
        </div>
      </header>

      {/* PHASE 1–4 EXISTING COMMAND CENTER */}
      <section className="space-y-6">
        <h2 className="text-lg font-bold text-slate-200 border-b border-slate-800 pb-2">Phase 1–4: Telemetry, Hotspots & Predictive Intelligence</h2>
        
        <DashboardMetrics observations={observations} />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <HotspotList hotspots={hotspots} />
          <ObservationList observations={observations} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <PredictionPanel forecast={forecast} plume={plume} />
          <ExposurePanel exposure={exposure} />
          <CorridorPanel corridors={corridors} />
        </div>
      </section>

      {/* PHASE 5: AI COMMAND CENTER & AUTHORITY RESPONSE */}
      <section className="space-y-6 pt-4 border-t border-slate-800">
        <h2 className="text-lg font-bold text-slate-200 border-b border-slate-800 pb-2">Phase 5: Gemini AI Intelligence & Authority Incident Response</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <AICommandCenter />
          <AuthorityResponse />
        </div>
      </section>

      {/* PHASE 6: FEDERATED LEARNING NETWORK */}
      <section className="space-y-6 pt-4 border-t border-slate-800">
        <h2 className="text-lg font-bold text-slate-200 border-b border-slate-800 pb-2">Phase 6: Federated Learning Network</h2>
        <FederatedLearningPanel />
      </section>
    </main>
  );
}
