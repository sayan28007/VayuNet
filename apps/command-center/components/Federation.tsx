"use client";

import type { FederationStatusResponse } from "@/types/api";

interface Props { federation: FederationStatusResponse | null; loading: boolean; error: string | null; }

export default function Federation({ federation, loading, error }: Props) {
  if (loading) return <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 text-sm text-slate-400">Loading federation status...</section>;
  if (error || !federation) return <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 text-sm text-amber-300">Unavailable</section>;
  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl">
      <h2 className="text-lg font-bold text-white">Federated Learning</h2>
      <p className="mb-4 text-xs text-slate-400">Global model and participating nodes</p>
      <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
        <div className="rounded-xl bg-slate-950 p-3"><span className="block text-[10px] text-slate-500">MODEL</span><span className="font-semibold text-cyan-300">{federation.global_model_version}</span></div>
        <div className="rounded-xl bg-slate-950 p-3"><span className="block text-[10px] text-slate-500">ROUND</span><span className="font-semibold text-white">{federation.current_round}</span></div>
        <div className="rounded-xl bg-slate-950 p-3"><span className="block text-[10px] text-slate-500">REGISTERED</span><span className="font-semibold text-white">{federation.registered_nodes}</span></div>
        <div className="rounded-xl bg-slate-950 p-3"><span className="block text-[10px] text-slate-500">HEALTHY</span><span className="font-semibold text-emerald-300">{federation.healthy_nodes}</span></div>
        <div className="rounded-xl bg-slate-950 p-3"><span className="block text-[10px] text-slate-500">STATUS</span><span className="font-semibold text-white">{federation.status}</span></div>
      </div>
      <div className="mt-3 text-xs text-slate-500">Last round: {federation.last_round ?? "None"}</div>
    </section>
  );
}
