import type {
  Hotspot,
  Alert,
  ForecastResponse,
  PlumeResponse,
  ExposureResponse,
  CorridorPrediction,
  FederationStatusResponse,
  AgentChatResponse,
  DemoResponse,
  CloudStatusResponse,
} from "@/types/api";

export type AlertAction = "acknowledge" | "action" | "resolve";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, options);
  if (!res.ok) {
    throw new Error(`API Error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export const api = {
  getHotspots(): Promise<Hotspot[]> { return fetchJson<Hotspot[]>(`${API_BASE}/hotspots`); },
  getAlerts(): Promise<Alert[]> { return fetchJson<Alert[]>(`${API_BASE}/alerts`); },
  updateAlertStatus(eventId: string, action: AlertAction): Promise<Alert> {
    return fetchJson<Alert>(`${API_BASE}/alerts/${eventId}/${action}`, { method: "POST" });
  },
  getForecast(hotspotId: string): Promise<ForecastResponse> {
    return fetchJson<ForecastResponse>(`${API_BASE}/predictions/forecast/${hotspotId}`);
  },
  getPlume(hotspotId: string): Promise<PlumeResponse> {
    return fetchJson<PlumeResponse>(`${API_BASE}/predictions/plume/${hotspotId}`);
  },
  getExposure(hotspotId: string): Promise<ExposureResponse> {
    return fetchJson<ExposureResponse>(`${API_BASE}/predictions/exposure/${hotspotId}`);
  },
  getCorridorPredictions(): Promise<CorridorPrediction[]> {
    return fetchJson<CorridorPrediction[]>(`${API_BASE}/predictions/corridors`);
  },
  getFederationStatus(): Promise<FederationStatusResponse> {
    return fetchJson<FederationStatusResponse>(`${API_BASE}/federation/status`);
  },
  chatWithAgent(message: string, language?: string): Promise<AgentChatResponse> {
    return fetchJson<AgentChatResponse>(`${API_BASE}/agent/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, language }),
    });
  },
  runDemo(): Promise<DemoResponse> { return fetchJson<DemoResponse>(`${API_BASE}/demo/run`, { method: "POST" }); },
  resetDemo(): Promise<DemoResponse> { return fetchJson<DemoResponse>(`${API_BASE}/demo/reset`, { method: "POST" }); },
  getCloudStatus(): Promise<CloudStatusResponse> {
    return fetchJson<CloudStatusResponse>(`${API_BASE}/cloud/status`);
  },
  syncObservationsToBigQuery(): Promise<{ status: string; inserted: number; errors: unknown[] }> {
    return fetchJson(`${API_BASE}/cloud/bigquery/sync`, { method: "POST" });
  },
};
