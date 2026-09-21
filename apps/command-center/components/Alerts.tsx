"use client";

import { useState } from "react";
import { api, type AlertAction } from "@/lib/api";
import type { Alert } from "@/types/api";

interface Props {
  alerts: Alert[] | null;
  loading: boolean;
  error: string | null;
  onAlertAction: (alert: Alert) => void;
}

export default function Alerts({ alerts, loading, error, onAlertAction }: Props) {
  const [busy, setBusy] = useState<string | null>(null);

  const runAction = async (alert: Alert, action: AlertAction) => {
    setBusy(alert.event_id);
    try {
      const updated = await api.updateAlertStatus(alert.event_id, action);
      onAlertAction(updated);
    } finally {
      setBusy(null);
    }
  };

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl">
      <div className="mb-4">
        <h2 className="text-lg font-bold text-white">Authority Response Alerts</h2>
        <p className="text-xs text-slate-400">State-machine controlled actions</p>
      </div>
      {loading && <div className="text-sm text-slate-400">Loading alerts...</div>}
      {!loading && error && <div className="text-sm text-amber-300">Unavailable</div>}
      {!loading && !error && (alerts?.length ?? 0) === 0 && <div className="text-sm text-slate-500">No active alerts.</div>}
      <div className="space-y-3">
        {(alerts ?? []).map((alert) => (
          <div key={alert.event_id} className="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
              <div>
                <div className="font-semibold text-white">{alert.event_id}</div>
                <div className="mt-1 text-xs text-slate-400">{alert.likely_source} · {alert.assigned_authority}</div>
              </div>
              <div className="text-xs font-semibold text-cyan-300">{alert.status}</div>
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-300 md:grid-cols-4">
              <span>Priority {alert.priority_level}</span>
              <span>Peak AQI {alert.predicted_peak}</span>
              <span>Population {alert.affected_population.toLocaleString()}</span>
              <span>Confidence {(alert.confidence * 100).toFixed(0)}%</span>
            </div>
            <div className="mt-3 text-xs text-slate-400">{alert.routing_reason}</div>
            <div className="mt-4 flex flex-wrap gap-2">
              {alert.status === "ROUTED" && (
                <button type="button" disabled={busy === alert.event_id} onClick={() => runAction(alert, "acknowledge")} className="rounded-lg bg-cyan-600 px-3 py-2 text-xs font-semibold text-white disabled:opacity-50">Acknowledge</button>
              )}
              {alert.status === "ACKNOWLEDGED" && (
                <button type="button" disabled={busy === alert.event_id} onClick={() => runAction(alert, "action")} className="rounded-lg bg-amber-600 px-3 py-2 text-xs font-semibold text-white disabled:opacity-50">Deploy Action</button>
              )}
              {alert.status === "ACTION_IN_PROGRESS" && (
                <button type="button" disabled={busy === alert.event_id} onClick={() => runAction(alert, "resolve")} className="rounded-lg bg-emerald-600 px-3 py-2 text-xs font-semibold text-white disabled:opacity-50">Resolve</button>
              )}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
