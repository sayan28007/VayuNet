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
  city?: string;
}
