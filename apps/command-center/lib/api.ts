import { config } from './config';
import { Observation } from '../types/observation';

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

  static async getCities(): Promise<string[]> {
    const res = await fetch(`${config.apiBaseUrl}/api/v1/cities`, { cache: 'no-store' });
    if (!res.ok) return [];
    return res.json();
  }
}

