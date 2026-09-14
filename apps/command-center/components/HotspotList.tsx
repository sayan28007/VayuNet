import type { Hotspot } from "../types/hotspot";
export default function HotspotList({hotspots}:{hotspots:Hotspot[]}){
 return <div className="space-y-3">{hotspots.map(h=><div key={h.hotspot_id} className="rounded-xl border border-white/10 p-4"><div className="flex justify-between"><div className="font-semibold">{h.city||"Unknown city"}</div><div className="text-xs uppercase">{h.severity}</div></div><div className="mt-2 text-sm">Score {(h.score*100).toFixed(1)}% · {h.evidence_count} evidence</div><div className="mt-2 text-xs text-slate-400">{h.explanation}</div></div>)}</div>
}
