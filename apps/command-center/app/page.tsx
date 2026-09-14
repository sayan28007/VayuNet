"use client";
import { useEffect,useState } from "react";
import DashboardMetrics from "../components/DashboardMetrics";
import HotspotList from "../components/HotspotList";
import { getHotspots } from "../lib/api";
import type { Hotspot } from "../types/hotspot";

export default function Home(){
 const [hotspots,setHotspots]=useState<Hotspot[]>([]);
 useEffect(()=>{getHotspots().then(setHotspots).catch(()=>setHotspots([]));},[]);
 return <main className="min-h-screen p-6"><div className="mx-auto max-w-6xl space-y-6"><div><h1 className="text-3xl font-bold">VayuNet Command Center</h1><p className="text-sm text-slate-400">Phase 3 · multimodal hotspot intelligence</p></div><DashboardMetrics hotspots={hotspots}/><section><HotspotList hotspots={hotspots}/></section></div></main>
}
