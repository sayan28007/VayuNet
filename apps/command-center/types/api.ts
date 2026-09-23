export type AlertStatus =
  | "DETECTED"
  | "VALIDATING"
  | "HIGH_CONFIDENCE"
  | "ROUTED"
  | "ACKNOWLEDGED"
  | "ACTION_IN_PROGRESS"
  | "RESOLVED";

export interface Hotspot {
  hotspot_id: string;
  latitude: number;
  longitude: number;
  score: number;
  confidence: number;
  severity: string;
  evidence_count: number;
  source_types: string[];
  pollutant_list: string[];
  anomaly_score: number;
  spatial_score: number;
  data_quality_score: number;
  explanation: string;
  city: string | null;
  metadata: Record<string, unknown>;
}

export interface Alert {
  event_id: string;
  hotspot_id: string;
  severity: string;
  priority_score: number;
  priority_level: string;
  location: { lat: number; lon: number };
  likely_source: string;
  confidence: number;
  affected_population: number;
  corridor: string;
  predicted_peak: number;
  assigned_authority: string;
  status: AlertStatus;
  routing_reason: string;
  recommended_response: string[];
  created_at: string;
  updated_at: string;
}

export interface ForecastPoint {
  horizon_minutes: number;
  predicted_aqi: number;
  confidence: number;
}

export interface ForecastResponse {
  hotspot_id: string;
  generated_at: string;
  model_name: string;
  forecasts: ForecastPoint[];
}

export interface PlumePoint {
  minutes: number;
  center_latitude: number;
  center_longitude: number;
  radius_km: number;
  intensity: number;
  polygon: { lat: number; lon: number }[];
}

export interface PlumeResponse {
  hotspot_id: string;
  generated_at: string;
  model: string;
  horizons: PlumePoint[];
}

export interface ExposureResponse {
  estimated_population: number;
  area_km2: number;
  confidence: number;
  data_source: string;
}

export interface CorridorPrediction {
  corridor_name: string;
  current_aqi: number;
  predicted_aqi_1h: number;
  predicted_aqi_2h: number;
  predicted_aqi_3h: number;
  predicted_peak_aqi: number;
  time_to_peak_minutes: number;
  risk_level: string;
  contributing_hotspot_id: string | null;
  confidence: number;
}

export interface FederationStatusResponse {
  status: string;
  global_model_version: string;
  current_round: number;
  registered_nodes: number;
  healthy_nodes: number;
  last_round: string | null;
  last_updated: string;
}

export interface AgentChatResponse {
  answer: string;
  tools_used: string[];
  grounding: unknown[];
  data_sources: unknown[];
  tool_selection_mode: string;
  language: string;
}

export interface DemoResponse {
  status: string;
  [key: string]: unknown;
}

export interface CloudServiceStatus {
  status: string;
  [key: string]: unknown;
}

export interface CloudStatusResponse {
  bigquery: CloudServiceStatus;
  secret_manager: CloudServiceStatus;
  vertex_ai: CloudServiceStatus;
  earth_engine: CloudServiceStatus;
}
