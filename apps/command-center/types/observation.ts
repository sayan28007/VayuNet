export type SourceType = 
  | 'citizen_report' 
  | 'local_sensor' 
  | 'official_monitor' 
  | 'meteorological' 
  | 'satellite' 
  | 'synthetic_demo';

export interface Observation {
  id: string;
  timestamp: string;
  latitude: number;
  longitude: number;
  source_type: SourceType;
  source_id: string;
  city?: string | null;
  corridor?: string | null;
  
  // Pollutants
  aqi?: number | null;
  pm25?: number | null;
  pm10?: number | null;
  no2?: number | null;
  so2?: number | null;
  co?: number | null;
  o3?: number | null;
  
  // Weather
  temperature?: number | null;
  humidity?: number | null;
  wind_speed?: number | null;
  wind_direction?: number | null;
  rainfall?: number | null;
  
  // Metadata
  confidence: number;
  data_quality_flag: boolean;
}

