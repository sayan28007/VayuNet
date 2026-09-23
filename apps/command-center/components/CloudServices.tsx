"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { CloudStatusResponse } from "@/types/api";

export default function CloudServices() {
  const [status, setStatus] = useState<CloudStatusResponse | null>(null);
  const [error, setError] = useState(false);
  const [syncing, setSyncing] = useState(false);
  const [syncMessage, setSyncMessage] = useState<string | null>(null);

  const loadStatus = () => {
    setError(false);
    api.getCloudStatus().then(setStatus).catch(() => setError(true));
  };

  useEffect(() => {
    loadStatus();
  }, []);

  const syncBigQuery = async () => {
    setSyncing(true);
    setSyncMessage(null);
    try {
      const result = await api.syncObservationsToBigQuery();
      setSyncMessage(`BigQuery sync: ${result.status}, ${result.inserted} rows inserted.`);
      loadStatus();
    } catch (e: unknown) {
      setSyncMessage(e instanceof Error ? e.message : "BigQuery sync failed");
    } finally {
      setSyncing(false);
    }
  };

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-lg font-bold text-white">Google Cloud Services</h2>
          <p className="text-xs text-slate-400">Cloud adapters and environment configuration</p>
        </div>
        <button type="button" onClick={syncBigQuery} disabled={syncing} className="rounded-xl bg-cyan-600 px-3 py-2 text-xs font-semibold text-white disabled:opacity-50">
          {syncing ? "Syncing..." : "Sync to BigQuery"}
        </button>
      </div>
      {error && <div className="mt-4 text-sm text-amber-300">Cloud status unavailable.</div>}
      {!error && !status && <div className="mt-4 text-sm text-slate-500">Loading cloud status...</div>}
      {status && (
        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {Object.entries(status).map(([name, value]) => (
            <div key={name} className="rounded-xl bg-slate-950 p-3">
              <span className="block text-[10px] uppercase tracking-wider text-slate-500">{name.replaceAll("_", " ")}</span>
              <span className={`mt-1 block text-sm font-semibold ${value.status === "configured" || value.status === "ready" ? "text-emerald-300" : "text-amber-300"}`}>
                {value.status}
              </span>
            </div>
          ))}
        </div>
      )}
      {syncMessage && <div className="mt-3 text-xs text-slate-400">{syncMessage}</div>}
    </section>
  );
}
