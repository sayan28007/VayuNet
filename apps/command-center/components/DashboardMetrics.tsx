"use client";
import type { Hotspot } from "../types/hotspot";
export default function DashboardMetrics({hotspots}:{hotspots:Hotspot[]}){
 const critical=hotspots.filter(h=>h.severity==="critical").length;
 return <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
  <div className="rounded-xl border border-white/10 p-4"><div className="text-xs text-slate-400">Hotspots</div><div className="text-2xl font-bold">{hotspots.length}</div></div>
  <div className="rounded-xl border border-white/10 p-4"><div className="text-xs text-slate-400">Critical</div><div className="text-2xl font-bold">{critical}</div></div>
  <div className="rounded-xl border border-white/10 p-4"><div className="text-xs text-slate-400">Evidence</div><div className="text-2xl font-bold">{hotspots.reduce((n,h)=>n+h.evidence_count,0)}</div></div>
  <div className="rounded-xl border border-white/10 p-4"><div className="text-xs text-slate-400">Pipeline</div><div className="text-2xl font-bold">Phase 3</div></div>
 </div>
}
