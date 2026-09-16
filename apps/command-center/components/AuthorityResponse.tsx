"use client";
import React, { useEffect, useState } from "react";
import api from "../lib/api";

interface Alert {
  event_id: string;
  hotspot_id: string;
  severity: string;
  priority_score: number;
  priority_level: string;
  likely_source: string;
  affected_population: number;
  corridor: string;
  predicted_peak: number;
  assigned_authority: string;
  status: string;
  routing_reason: string;
  recommended_response: string[];
}

export default function AuthorityResponse() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAlerts = async () => {
    try {
      const data = await api.getAlerts();
      setAlerts(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  const updateStatus = async (eventId: string, action: string) => {
    try {
      if (action === "acknowledge") {
        await api.acknowledgeAlert(eventId);
      } else if (action === "action") {
        await api.startAlertAction(eventId);
      } else if (action === "resolve") {
        await api.resolveAlert(eventId);
      }
      await fetchAlerts();
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) return <div className="text-slate-400 p-4">Loading operational incidents...</div>;
  if (error) return <div className="text-red-400 p-4">Error: {error}</div>;

  return (
    <div className="bg-slate-900 text-white p-6 rounded-xl border border-slate-700 shadow-xl">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        🚨 Authority Incident Response Center
      </h2>
      <div className="space-y-4">
        {alerts.length === 0 ? (
          <p className="text-slate-400 text-sm">No active incidents found.</p>
        ) : (
          alerts.map((alert) => (
            <div key={alert.event_id} className="bg-slate-950 p-5 rounded-lg border border-slate-800 space-y-3">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-xs font-mono text-cyan-400 font-semibold">{alert.event_id}</span>
                  <h3 className="text-base font-bold text-white">{alert.likely_source}</h3>
                </div>
                <div className="flex gap-2">
                  <span className="px-2.5 py-1 rounded text-xs font-bold bg-amber-900/60 text-amber-200 border border-amber-700">
                    {alert.priority_level}
                  </span>
                  <span className="px-2.5 py-1 rounded text-xs font-bold bg-slate-800 text-slate-300">
                    Status: {alert.status}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs bg-slate-900 p-3 rounded border border-slate-800">
                <div><strong className="text-slate-400 block">Authority:</strong> {alert.assigned_authority}</div>
                <div><strong className="text-slate-400 block">Corridor:</strong> {alert.corridor}</div>
                <div><strong className="text-slate-400 block">Peak AQI:</strong> {alert.predicted_peak}</div>
                <div><strong className="text-slate-400 block">Population:</strong> {alert.affected_population?.toLocaleString()}</div>
              </div>

              <p className="text-xs text-slate-300"><strong>Routing Reason:</strong> {alert.routing_reason}</p>

              {alert.recommended_response?.length > 0 && (
                <div className="text-xs bg-cyan-950/40 p-3 rounded border border-cyan-900/50">
                  <strong className="text-cyan-300 block mb-1">Recommended Response Actions:</strong>
                  <ul className="list-disc list-inside space-y-1 text-slate-300">
                    {alert.recommended_response.map((rec, i) => (
                      <li key={i}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="flex gap-2 pt-2 border-t border-slate-800">
                {alert.status === "HIGH_CONFIDENCE" && (
                  <button
                    onClick={() => updateStatus(alert.event_id, "acknowledge")}
                    className="bg-blue-600 hover:bg-blue-500 text-white px-3 py-1.5 rounded text-xs font-semibold"
                  >
                    ACKNOWLEDGE
                  </button>
                )}
                {alert.status === "ACKNOWLEDGED" && (
                  <button
                    onClick={() => updateStatus(alert.event_id, "action")}
                    className="bg-amber-600 hover:bg-amber-500 text-white px-3 py-1.5 rounded text-xs font-semibold"
                  >
                    START ACTION
                  </button>
                )}
                {alert.status === "ACTION_IN_PROGRESS" && (
                  <button
                    onClick={() => updateStatus(alert.event_id, "resolve")}
                    className="bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded text-xs font-semibold"
                  >
                    RESOLVE
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
