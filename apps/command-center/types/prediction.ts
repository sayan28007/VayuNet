export interface PlumeHorizon {
  minutes: number;
  center_latitude: number;
  center_longitude: number;
  radius_km: number;
  intensity: number;
  polygon: { lat: number; lon: number }[];
}

export interface PlumePrediction {
  hotspot_id: string;
  generated_at: string;
  model: string;
  horizons: PlumeHorizon[];
}

export interface ForecastPoint {
  horizon_minutes: number;
  predicted_aqi: number;
  confidence: number;
}

export interface AQIForecast {
  hotspot_id: string;
  generated_at: string;
  model_name: string;
  forecasts: ForecastPoint[];
}

export interface CorridorRisk {
  corridor_name: string;
  current_aqi: number;
  predicted_aqi_1h: number;
  predicted_aqi_2h: number;
  predicted_aqi_3h: number;
  predicted_peak_aqi: number;
  time_to_peak_minutes: number;
  risk_level: 'critical' | 'high' | 'moderate' | 'low';
  contributing_hotspot_id?: string;
  confidence: number;
}

export interface PopulationExposure {
  estimated_population: number;
  area_km2: number;
  confidence: number;
  data_source: string;
}
