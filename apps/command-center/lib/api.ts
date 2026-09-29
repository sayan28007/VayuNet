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

export type AlertAction = "route" | "acknowledge" | "action" | "resolve";

const now = "2026-09-29T10:00:00.000Z";

const hotspots: Hotspot[] = [
  { hotspot_id: "HS-VIZ-001", latitude: 17.6868, longitude: 83.2185, score: 0.86, confidence: 0.92, severity: "HIGH", evidence_count: 8, source_types: ["local_sensor", "citizen_report", "official_monitor"], pollutant_list: ["AQI", "PM2.5", "NO2"], anomaly_score: 0.88, spatial_score: 0.79, data_quality_score: 0.94, explanation: "Converging sensor, citizen and official signals indicate a high-confidence urban pollution hotspot.", city: "Visakhapatnam", metadata: { source: "standalone_demo" } },
  { hotspot_id: "HS-DEL-002", latitude: 28.6139, longitude: 77.209, score: 0.78, confidence: 0.87, severity: "HIGH", evidence_count: 11, source_types: ["local_sensor", "official_monitor", "satellite"], pollutant_list: ["AQI", "PM2.5", "NO2"], anomaly_score: 0.81, spatial_score: 0.73, data_quality_score: 0.91, explanation: "Multiple independent signals align around an elevated pollution cluster.", city: "Delhi", metadata: { source: "standalone_demo" } },
  { hotspot_id: "HS-MUM-003", latitude: 19.076, longitude: 72.8777, score: 0.64, confidence: 0.81, severity: "MEDIUM", evidence_count: 6, source_types: ["local_sensor", "citizen_report"], pollutant_list: ["AQI", "PM2.5"], anomaly_score: 0.67, spatial_score: 0.61, data_quality_score: 0.86, explanation: "A persistent but moderate cluster is visible across local observations.", city: "Mumbai", metadata: { source: "standalone_demo" } },
];

let alerts: Alert[] = [
  { event_id: "EVT-HS-VIZ-001", hotspot_id: "HS-VIZ-001", severity: "HIGH", priority_score: 91, priority_level: "P1", location: { lat: 17.6868, lon: 83.2185 }, likely_source: "Industrial Emission", confidence: 0.92, affected_population: 84500, corridor: "Visakhapatnam Industrial Corridor", predicted_peak: 364, assigned_authority: "State Pollution Control Board", status: "HIGH_CONFIDENCE", routing_reason: "High predicted AQI with high-confidence multimodal evidence.", recommended_response: ["Route field team", "Verify stationary sensor telemetry"], created_at: now, updated_at: now },
  { event_id: "EVT-HS-DEL-002", hotspot_id: "HS-DEL-002", severity: "HIGH", priority_score: 84, priority_level: "P1", location: { lat: 28.6139, lon: 77.209 }, likely_source: "Regional Smog Cluster", confidence: 0.87, affected_population: 142000, corridor: "Delhi NCR Mobility Corridor", predicted_peak: 418, assigned_authority: "Municipal Emergency Cell", status: "ROUTED", routing_reason: "Exposure footprint overlaps a high-density corridor.", recommended_response: ["Acknowledge incident", "Coordinate traffic response"], created_at: now, updated_at: now },
  { event_id: "EVT-HS-MUM-003", hotspot_id: "HS-MUM-003", severity: "MEDIUM", priority_score: 66, priority_level: "P2", location: { lat: 19.076, lon: 72.8777 }, likely_source: "Urban Activity", confidence: 0.81, affected_population: 59200, corridor: "Mumbai Coastal Mobility Corridor", predicted_peak: 276, assigned_authority: "Municipal Response Cell", status: "ACTION_IN_PROGRESS", routing_reason: "Moderate hotspot with sustained upward trend.", recommended_response: ["Monitor plume", "Review local traffic conditions"], created_at: now, updated_at: now },
];

let federation: FederationStatusResponse = { status: "healthy", global_model_version: "fedavg-v1.4.2", current_round: 8, registered_nodes: 3, healthy_nodes: 3, last_round: now, last_updated: now };

const corridors: CorridorPrediction[] = [
  { corridor_name: "Visakhapatnam Industrial Corridor", current_aqi: 284, predicted_aqi_1h: 302, predicted_aqi_2h: 326, predicted_aqi_3h: 341, predicted_peak_aqi: 364, time_to_peak_minutes: 178, risk_level: "HIGH", contributing_hotspot_id: "HS-VIZ-001", confidence: 0.9 },
  { corridor_name: "Delhi NCR Mobility Corridor", current_aqi: 342, predicted_aqi_1h: 361, predicted_aqi_2h: 389, predicted_aqi_3h: 405, predicted_peak_aqi: 418, time_to_peak_minutes: 142, risk_level: "HIGH", contributing_hotspot_id: "HS-DEL-002", confidence: 0.88 },
  { corridor_name: "Mumbai Coastal Mobility Corridor", current_aqi: 236, predicted_aqi_1h: 249, predicted_aqi_2h: 258, predicted_aqi_3h: 271, predicted_peak_aqi: 276, time_to_peak_minutes: 164, risk_level: "MEDIUM", contributing_hotspot_id: "HS-MUM-003", confidence: 0.82 },
];

const clone = <T,>(value: T): T => JSON.parse(JSON.stringify(value)) as T;
const forecast = (id: string, base: number): ForecastResponse => ({ hotspot_id: id, generated_at: now, model_name: "VayuNet AQI Forecast", forecasts: [30, 60, 120, 180, 360].map((m, i) => ({ horizon_minutes: m, predicted_aqi: base + [12, 24, 39, 54, 33][i], confidence: [0.94, 0.91, 0.87, 0.82, 0.76][i] })) });
const plume = (id: string, lat: number, lon: number): PlumeResponse => ({ hotspot_id: id, generated_at: now, model: "Wind-aware plume spread model", horizons: [30, 60, 120, 180, 360].map(m => ({ minutes: m, center_latitude: lat + m * 0.00005, center_longitude: lon + m * 0.00011, radius_km: 1.1 + m / 120, intensity: Math.max(0.18, 0.86 - m / 900), polygon: [] })) });
const forecasts: Record<string, ForecastResponse> = { "HS-VIZ-001": forecast("HS-VIZ-001", 284), "HS-DEL-002": forecast("HS-DEL-002", 342), "HS-MUM-003": forecast("HS-MUM-003", 236) };
const plumes: Record<string, PlumeResponse> = { "HS-VIZ-001": plume("HS-VIZ-001", 17.6868, 83.2185), "HS-DEL-002": plume("HS-DEL-002", 28.6139, 77.209), "HS-MUM-003": plume("HS-MUM-003", 19.076, 72.8777) };
const exposure: Record<string, ExposureResponse> = { "HS-VIZ-001": { estimated_population: 84500, area_km2: 19.8, confidence: 0.88, data_source: "standalone demo model" }, "HS-DEL-002": { estimated_population: 142000, area_km2: 32.6, confidence: 0.84, data_source: "standalone demo model" }, "HS-MUM-003": { estimated_population: 59200, area_km2: 15.4, confidence: 0.79, data_source: "standalone demo model" } };

const demo = process.env.NEXT_PUBLIC_DEMO_MODE !== "false";
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> { const res = await fetch(url, options); if (!res.ok) throw new Error(`API Error: ${res.status} ${res.statusText}`); return res.json(); }
function alertUpdate(eventId: string, action: AlertAction): Alert { const item = alerts.find(a => a.event_id === eventId); if (!item) throw new Error("Demo alert not found"); const next: Record<AlertAction, Alert["status"]> = { route: "ROUTED", acknowledge: "ACKNOWLEDGED", action: "ACTION_IN_PROGRESS", resolve: "RESOLVED" }; item.status = next[action]; item.updated_at = new Date().toISOString(); return clone(item); }

export const api = {
  getHotspots(): Promise<Hotspot[]> { return demo ? Promise.resolve(clone(hotspots)) : fetchJson(`${API_BASE}/hotspots`); },
  getAlerts(): Promise<Alert[]> { return demo ? Promise.resolve(clone(alerts)) : fetchJson(`${API_BASE}/alerts`); },
  updateAlertStatus(eventId: string, action: AlertAction): Promise<Alert> { return demo ? Promise.resolve(alertUpdate(eventId, action)) : fetchJson(`${API_BASE}/alerts/${eventId}/${action}`, { method: "POST" }); },
  getForecast(id: string): Promise<ForecastResponse> { return demo ? Promise.resolve(clone(forecasts[id])) : fetchJson(`${API_BASE}/predictions/forecast/${id}`); },
  getPlume(id: string): Promise<PlumeResponse> { return demo ? Promise.resolve(clone(plumes[id])) : fetchJson(`${API_BASE}/predictions/plume/${id}`); },
  getExposure(id: string): Promise<ExposureResponse> { return demo ? Promise.resolve(clone(exposure[id])) : fetchJson(`${API_BASE}/predictions/exposure/${id}`); },
  getCorridorPredictions(): Promise<CorridorPrediction[]> { return demo ? Promise.resolve(clone(corridors)) : fetchJson(`${API_BASE}/predictions/corridors`); },
  getFederationStatus(): Promise<FederationStatusResponse> { return demo ? Promise.resolve(clone(federation)) : fetchJson(`${API_BASE}/federation/status`); },
  chatWithAgent(message: string, language?: string): Promise<AgentChatResponse> { if (demo) return Promise.resolve({ answer: language === "hi" ? "Visakhapatnam hotspot high-confidence hai, predicted peak AQI 364 hai aur authority routing ready hai." : language === "te" ? "Visakhapatnam hotspot high-confidence signal. Predicted peak AQI 364 aur authority routing ready ga undi." : `Demo-grounded analysis for "${message}": Visakhapatnam has a high-confidence hotspot with predicted peak AQI 364 and authority routing ready.`, tools_used: ["get_active_hotspots", "get_forecast", "get_authority_status"], grounding: clone(hotspots.slice(0, 2)), data_sources: ["standalone_demo_dataset"], tool_selection_mode: "demo_fallback", language: language || "en" }); return fetchJson(`${API_BASE}/agent/chat`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message, language }) }); },
  runDemo(): Promise<DemoResponse> { if (demo) { federation = { ...federation, current_round: federation.current_round + 1 }; alerts = clone(alerts); return Promise.resolve({ status: "demo_completed", hotspot_count: hotspots.length, alert_count: alerts.length, federation_round: federation.current_round }); } return fetchJson(`${API_BASE}/demo/run`, { method: "POST" }); },
  resetDemo(): Promise<DemoResponse> { if (demo) { federation = { status: "healthy", global_model_version: "fedavg-v1.4.2", current_round: 8, registered_nodes: 3, healthy_nodes: 3, last_round: now, last_updated: now }; return Promise.resolve({ status: "demo_reset", hotspot_count: hotspots.length, alert_count: alerts.length }); } return fetchJson(`${API_BASE}/demo/reset`, { method: "POST" }); },
  getCloudStatus(): Promise<CloudStatusResponse> { if (demo) return Promise.resolve({ bigquery: { status: "demo_ready" }, secret_manager: { status: "demo_ready" }, vertex_ai: { status: "demo_mode" }, earth_engine: { status: "demo_ready" } }); return fetchJson(`${API_BASE}/cloud/status`); },
  syncObservationsToBigQuery(): Promise<{ status: string; inserted: number; errors: unknown[] }> { return demo ? Promise.resolve({ status: "demo_synced", inserted: 18, errors: [] }) : fetchJson(`${API_BASE}/cloud/bigquery/sync`, { method: "POST" }); },
  postAgentChat(message: string, language = "en"): Promise<AgentChatResponse> { return this.chatWithAgent(message, language); },
  acknowledgeAlert(id: string): Promise<Alert> { return this.updateAlertStatus(id, "acknowledge"); },
  startAlertAction(id: string): Promise<Alert> { return this.updateAlertStatus(id, "action"); },
  resolveAlert(id: string): Promise<Alert> { return this.updateAlertStatus(id, "resolve"); },
  getFederationNodes(): Promise<unknown[]> { return demo ? Promise.resolve([{ city: "Delhi", status: "healthy", local_samples: 1240 }, { city: "Visakhapatnam", status: "healthy", local_samples: 980 }, { city: "Mumbai", status: "healthy", local_samples: 1110 }]) : fetchJson(`${API_BASE}/federation/nodes`); },
  getFederationRounds(): Promise<unknown[]> { return demo ? Promise.resolve([{ round: 8, version: "fedavg-v1.4.2", status: "completed" }, { round: 7, version: "fedavg-v1.4.1", status: "completed" }]) : fetchJson(`${API_BASE}/federation/rounds`); },
  runFederationRound(): Promise<unknown> { if (demo) { federation = { ...federation, current_round: federation.current_round + 1 }; return Promise.resolve({ status: "completed", round: federation.current_round }); } return fetchJson(`${API_BASE}/federation/round`, { method: "POST" }); },
};

export default api;
