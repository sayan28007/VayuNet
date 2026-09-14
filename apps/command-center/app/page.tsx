'use client';
import React, { useEffect, useState } from 'react';
import { ApiClient } from '@/lib/api';
import { Observation } from '@/types/observation';
import { DashboardMetrics } from '@/components/DashboardMetrics';
import { ObservationList } from '@/components/ObservationList';

export default function Dashboard() {
  const [health, setHealth] = useState<string>('Connecting...');
  const [observations, setObservations] = useState<Observation[]>([]);
  const [cities, setCities] = useState<string[]>([]);
  const [selectedCity, setSelectedCity] = useState<string>('');

  useEffect(() => {
    ApiClient.getHealth()
      .then(data => setHealth(data.status))
      .catch(() => setHealth('Offline'));

    ApiClient.getCities()
      .then(setCities)
      .catch(console.error);
  }, []);

  useEffect(() => {
    ApiClient.getObservations(selectedCity || undefined)
      .then(setObservations)
      .catch(console.error);
  }, [selectedCity]);

  return (
    <main className="p-6 max-w-[1600px] mx-auto w-full space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">VayuNet Command Center</h1>
        <span className="text-sm px-3 py-1 bg-slate-800 rounded-full border border-slate-700">
          API: {health}
        </span>
      </div>

      <DashboardMetrics observations={observations} />

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">Live Observations</h2>
          <select 
            className="bg-slate-900 border border-slate-700 text-white text-sm rounded-lg p-2"
            value={selectedCity}
            onChange={(e) => setSelectedCity(e.target.value)}
          >
            <option value="">All Cities</option>
            {cities.map(city => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>
        </div>
        
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
          <ObservationList observations={observations} />
        </div>
      </div>
    </main>
  );
}

