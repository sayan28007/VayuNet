"use client";

import type { Alert, FederationStatusResponse, Hotspot } from "@/types/api";

interface Props {
  hotspots: Hotspot[] | null;
  alerts: Alert[] | null;
  federation: FederationStatusResponse | null;
}

export default function Overview({ hotspots, alerts, federation }: Props) {
  const cards = [
    ["Active Hotspots", hotspots?.length ?? 0],
    ["Active Alerts", alerts?.filter((a) => a.status !== "RESOLVED").length ?? 0],
    ["Healthy Nodes", federation ? `${federation.healthy_nodes}/${federation.registered_nodes}` : 0],
    ["Model Version", federation?.global_model_version ?? "Unavailable"],
  ];

  return (
    <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {cards.map(([label, value]) => (
        <div key={label} className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl">
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-500">{label}</div>
          <div className="mt-2 text-2xl font-black text-white">{value}</div>
        </div>
      ))}
    </section>
  );
}
