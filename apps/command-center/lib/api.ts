import { API_BASE_URL } from "./config";
import type { Observation } from "../types/observation";
import type { Hotspot } from "../types/hotspot";

export async function getObservations(): Promise<Observation[]> {
  const res=await fetch(`${API_BASE_URL}/api/v1/observations`,{cache:"no-store"});
  if(!res.ok) throw new Error("Failed to load observations");
  return res.json();
}
export async function getHotspots(): Promise<Hotspot[]> {
  const res=await fetch(`${API_BASE_URL}/api/v1/hotspots`,{cache:"no-store"});
  if(!res.ok) throw new Error("Failed to load hotspots");
  return res.json();
}
