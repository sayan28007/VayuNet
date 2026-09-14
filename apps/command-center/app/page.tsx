'use client';
import React, { useEffect, useState } from 'react';
import { ApiClient } from '@/lib/api';
import { Observation } from '@/types/observation';
import { Hotspot } from '@/types/hotspot';
import { AQIForecast, PlumePrediction, CorridorRisk, PopulationExposure } from '@/types/prediction';
import { DashboardMetrics } from '@/components/DashboardMetrics';
import { ObservationList } from '@/components/ObservationList';
import { HotspotList } from '@/components/HotspotList';
import { PredictionPanel } from '@/components/PredictionPanel';
import { CorridorPanel } from '@/components/CorridorPanel';
import { ExposurePanel } from '@/components/ExposurePanel';

export default function Dashboard() {
  const [health, setHealth] = useState<string>('Connecting...');
  const [observations, setObservations] = useState<Observation[]>([]);
  const [hotspots, setHotspots] = useState<Hotspot[]>([]);
  const [forecast, setForecast] = useState<AQIForecast>();
  const [plume, setPlume] = useState<PlumePrediction>();
  const [corridors, setCorridors] = useState<CorridorRisk[]>([]);
  const [exposure, setExposure] = useState<PopulationExposure>();
  const [view, setView] = useState<'intelligence' | 'corridors' | 'raw'>('intelligence');

  useEffect(() => {
    ApiClient.getHealth()
      .then(data => setHealth(data.status))
      .catch(() => setHealth('Offline'));

    ApiClient.getObservations()
      .then(setObservations)
      .catch(console.error);
      
    ApiClient.getHotspots()
      .then(async (hsList) => {
        setHotspots(hsList);
        if (hsList.length > 0) {
          const topId = hsList[0].hotspot_id;
          const [f, p, e] = await Promise.all([
            ApiClient.getForecast(topId).catch(() => undefined),
            ApiClient.getPlume(topId).catch(() => undefined),
            ApiClient.getExposure(topId).catch(() => undefined)
          ]);
          if (f) setForecast(f);
          if (p) setPlume(p);
          if (e) setExposure(e);
        }
      })
      .catch(console.error);

    ApiClient.getCorridors()
      .then(setCorridors)
      .catch(console.error);
  }, []);

  return (
    <main className="p-6 max-w-[1600px] mx-auto w-full space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">VayuNet Command Center — Phase 4 Prediction Engine</h1>
        <span className="text-sm px-3 py-1 bg-slate-800 rounded-full border border-slate-700 text-slate-300">
          API: {health}
        </span>
      </div>

      <DashboardMetrics observations={observations} hotspots={hotspots} />

      <div className="space-y-4">
        <div className="flex items-center space-x-4 border-b border-slate-800 pb-2">
          <button 
            className={`px-4 py-2 font-semibold ${view === 'intelligence' ? 'text-white border-b-2 border-blue-500' : 'text-slate-500'}`}
            onClick={() => setView('intelligence')}
          >
            Hotspot Intelligence & Plume/Forecasts
          </button>
          <button 
            className={`px-4 py-2 font-semibold ${view === 'corridors' ? 'text-white border-b-2 border-blue-500' : 'text-slate-500'}`}
            onClick={() => setView('corridors')}
          >
            Economic Corridors & Exposure
          </button>
          <button 
            className={`px-4 py-2 font-semibold ${view === 'raw' ? 'text-white border-b-2 border-blue-500' : 'text-slate-500'}`}
            onClick={() => setView('raw')}
          >
            Raw Observations
          </button>
        </div>
        
        {view === 'intelligence' && (
          <div className="space-y-6">
            <PredictionPanel forecast={forecast} plume={plume} />
            <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-bold text-white mb-4">Active Hotspot Candidates</h3>
              <HotspotList hotspots={hotspots} />
            </div>
          </div>
        )}

        {view === 'corridors' && (
          <div className="space-y-6">
            <CorridorPanel corridors={corridors} />
            <ExposurePanel exposure={exposure} />
          </div>
        )}

        {view === 'raw' && (
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
            <ObservationList observations={observations} />
          </div>
        )}
      </div>
    </main>
  );
}
