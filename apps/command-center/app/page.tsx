"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";
import type { Alert, FederationStatusResponse, Hotspot } from "@/types/api";
import Alerts from "@/components/Alerts";
import Predictions from "@/components/Predictions";
import Corridors from "@/components/Corridors";
import Federation from "@/components/Federation";
import GeminiPanel from "@/components/GeminiPanel";
import Overview from "@/components/Overview";
import Hotspots from "@/components/Hotspots";
import OperationalMap from "@/components/OperationalMap";
import DemoHero from "@/components/DemoHero";
import DemoFlow from "@/components/DemoFlow";
import ImpactStory from "@/components/ImpactStory";
import CitySelector from "@/components/CitySelector";

type CityOption = { name: string };

const DEFAULT_CITIES: CityOption[] = [
  { name: "Visakhapatnam" },
  { name: "Delhi" },
  { name: "Mumbai" },
];

export default function CommandCenterPage() {
  const [hotspots, setHotspots] = useState<Hotspot[] | null>(null);
  const [hotspotsError, setHotspotsError] = useState<string | null>(null);
  const [hotspotsLoading, setHotspotsLoading] = useState(true);
  const [selectedHotspotId, setSelectedHotspotId] = useState("");
  const [alerts, setAlerts] = useState<Alert[] | null>(null);
  const [alertsError, setAlertsError] = useState<string | null>(null);
  const [alertsLoading, setAlertsLoading] = useState(true);
  const [federation, setFederation] = useState<FederationStatusResponse | null>(null);
  const [federationError, setFederationError] = useState<string | null>(null);
  const [federationLoading, setFederationLoading] = useState(true);
  const [demoLoading, setDemoLoading] = useState(false);
  const [demoError, setDemoError] = useState<string | null>(null);
  const [cities, setCities] = useState<CityOption[]>(DEFAULT_CITIES);
  const [selectedCity, setSelectedCity] = useState("All Cities");

  const fetchHotspotsData = useCallback(async () => {
    setHotspotsLoading(true);
    setHotspotsError(null);
    try {
      const data = await api.getHotspots();
      setHotspots(data);
    } catch (e: unknown) {
      setHotspotsError(e instanceof Error ? e.message : "Unavailable");
      setHotspots(null);
    } finally {
      setHotspotsLoading(false);
    }
  }, []);

  const fetchAlertsData = useCallback(async () => {
    setAlertsLoading(true);
    setAlertsError(null);
    try { setAlerts(await api.getAlerts()); }
    catch (e: unknown) { setAlertsError(e instanceof Error ? e.message : "Unavailable"); setAlerts(null); }
    finally { setAlertsLoading(false); }
  }, []);

  const fetchFederationData = useCallback(async () => {
    setFederationLoading(true);
    setFederationError(null);
    try { setFederation(await api.getFederationStatus()); }
    catch (e: unknown) { setFederationError(e instanceof Error ? e.message : "Unavailable"); setFederation(null); }
    finally { setFederationLoading(false); }
  }, []);

  useEffect(() => {
    fetchHotspotsData();
    fetchAlertsData();
    fetchFederationData();

    try {
      const stored = localStorage.getItem("vayunet-cities");
      if (stored) {
        const parsed = JSON.parse(stored) as CityOption[];
        if (Array.isArray(parsed) && parsed.length) setCities(parsed);
      }
    } catch {
      // keep defaults
    }
  }, [fetchHotspotsData, fetchAlertsData, fetchFederationData]);

  const addCity = (name: string) => {
    setCities((current) => {
      if (current.some((city) => city.name.toLowerCase() === name.toLowerCase())) return current;
      const next = [...current, { name }].sort((a, b) => a.name.localeCompare(b.name));
      localStorage.setItem("vayunet-cities", JSON.stringify(next));
      return next;
    });
  };

  const filteredHotspots = useMemo(() => {
    if (!hotspots) return null;
    if (selectedCity === "All Cities") return hotspots;
    return hotspots.filter((hotspot) => hotspot.city?.toLowerCase() === selectedCity.toLowerCase());
  }, [hotspots, selectedCity]);

  const filteredAlerts = useMemo(() => {
    if (!alerts) return null;
    if (selectedCity === "All Cities") return alerts;
    const cityHotspotIds = new Set((filteredHotspots ?? []).map((hotspot) => hotspot.hotspot_id));
    return alerts.filter((alert) => cityHotspotIds.has(alert.hotspot_id));
  }, [alerts, filteredHotspots, selectedCity]);

  useEffect(() => {
    const first = filteredHotspots?.[0];
    setSelectedHotspotId(first?.hotspot_id ?? "");
  }, [filteredHotspots]);

  const refreshAll = async () => {
    await Promise.all([fetchHotspotsData(), fetchAlertsData(), fetchFederationData()]);
  };

  const runDemo = async () => {
    setDemoLoading(true);
    setDemoError(null);
    try { await api.runDemo(); await refreshAll(); }
    catch (e: unknown) { setDemoError(e instanceof Error ? e.message : "Demo run failed"); }
    finally { setDemoLoading(false); }
  };

  const resetDemo = async () => {
    setDemoLoading(true);
    setDemoError(null);
    try { await api.resetDemo(); await refreshAll(); }
    catch (e: unknown) { setDemoError(e instanceof Error ? e.message : "Demo reset failed"); }
    finally { setDemoLoading(false); }
  };

  const handleAlertAction = (updated: Alert) => {
    setAlerts((current) => (current ?? []).map((alert) =>
      alert.event_id === updated.event_id ? updated : alert
    ));
  };

  return (
    <main className="min-h-screen space-y-6 bg-slate-950 p-4 text-slate-100 sm:p-8">
      <header className="flex flex-col gap-4 border-b border-slate-800 pb-6 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-black tracking-tight text-white">VayuNet Command Center</h1>
          <p className="mt-1 text-sm text-slate-400">Hyperlocal pollution intelligence, prediction, response and federated climate action</p>
        </div>
        <div className="text-right text-xs text-slate-500">Final demo build</div>
      </header>

      <CitySelector cities={cities} selectedCity={selectedCity} onSelectCity={setSelectedCity} onAddCity={addCity} />
      <DemoHero onRunDemo={runDemo} onResetDemo={resetDemo} loading={demoLoading} />
      {demoError && <div className="rounded-xl border border-amber-800 bg-amber-950/30 p-3 text-sm text-amber-300">{demoError}</div>}

      <Overview hotspots={filteredHotspots} alerts={filteredAlerts} federation={federation} />
      <DemoFlow />
      <div className="grid gap-6 lg:grid-cols-2">
        <Hotspots hotspots={filteredHotspots} loading={hotspotsLoading} error={hotspotsError} selectedHotspotId={selectedHotspotId} onSelectHotspot={setSelectedHotspotId} />
        <OperationalMap hotspots={filteredHotspots} />
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <Predictions hotspotId={selectedHotspotId} />
        <Corridors />
      </div>
      <ImpactStory />
      <Federation federation={federation} loading={federationLoading} error={federationError} />
      <Alerts alerts={filteredAlerts} loading={alertsLoading} error={alertsError} onAlertAction={handleAlertAction} />
      <GeminiPanel />
    </main>
  );
}
