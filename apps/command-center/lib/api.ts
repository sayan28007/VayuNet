import { config } from './config';
import { Observation } from '../types/observation';
import { Hotspot } from '../types/hotspot';
import { PlumePrediction, AQIForecast, CorridorRisk, PopulationExposure } from '../types/prediction';

export class ApiClient {
  static async getHealth() {
    const res = await fetch(`${config.apiBaseUrl}/api/v1/health`);
    return res.json();
  }

  static async getObservations(city?: string): Promise<Observation[]> {
    const url = new URL(`${config.apiBaseUrl}/api/v1/observations`);
    if (city) url.searchParams.append('city', city);
    const res = await fetch(url.toString(), { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch observations');
    return res.json();
  }

  static async getHotspots(): Promise<Hotspot[]> {
    const res = await fetch(`${config.apiBaseUrl}/api/v1/hotspots`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch intelligence hotspots');
    return res.json();
  }

  static async getPlume(hotspotId: string): Promise<PlumePrediction> {
    const res = await fetch(`${config.apiBaseUrl}/api/v1/predictions/plume/${hotspotId}`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch plume prediction');
    return res.json();
  }

  static async getForecast(hotspotId: string): Promise<AQIForecast> {
    const res = await fetch(`${config.apiBaseUrl}/api/v1/predictions/forecast/${hotspotId}`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch AQI forecast');
    return res.json();
  }

  static async getCorridors(): Promise<CorridorRisk[]> {
    const res = await fetch(`${config.apiBaseUrl}/api/v1/predictions/corridors`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch corridor risks');
    return res.json();
  }

  static async getExposure(hotspotId: string): Promise<PopulationExposure> {
    const res = await fetch(`${config.apiBaseUrl}/api/v1/predictions/exposure/${hotspotId}`, { cache: 'no-store' });
    if (!res.ok) throw new Error('Failed to fetch population exposure');
    return res.json();
  }
}
