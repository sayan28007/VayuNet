import React, { useState } from 'react';
import { AQIForecast, PlumePrediction } from '../types/prediction';

interface Props {
  forecast?: AQIForecast;
  plume?: PlumePrediction;
}

export function PredictionPanel({ forecast, plume }: Props) {
  const [selectedHorizonMinutes, setSelectedHorizonMinutes] = useState<number>(30);

  if (!forecast || !plume) return <p className="text-slate-500 p-4">Loading prediction engines...</p>;

  const currentForecastPoint = forecast.forecasts.find(f => f.horizon_minutes === selectedHorizonMinutes) || forecast.forecasts[0];
  const currentPlumeHorizon = plume.horizons.find(h => h.minutes === selectedHorizonMinutes) || plume.horizons[0];

  const horizons = [30, 60, 120, 180, 360];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h3 className="text-lg font-bold text-white">Prediction Engine (Phase 4)</h3>
          <p className="text-sm text-slate-400">Model: {forecast.model_name} | Plume: {plume.model}</p>
        </div>
        
        {/* Timeline Selector */}
        <div className="flex space-x-2 bg-slate-950 p-1.5 rounded-lg border border-slate-800">
          <button 
            onClick={() => setSelectedHorizonMinutes(0)}
            className={`px-3 py-1 text-xs font-semibold rounded ${selectedHorizonMinutes === 0 ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}
          >
            NOW
          </button>
          {horizons.map(m => (
            <button
              key={m}
              onClick={() => setSelectedHorizonMinutes(m)}
              className={`px-3 py-1 text-xs font-semibold rounded ${selectedHorizonMinutes === m ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'}`}
            >
              +{m >= 60 ? `${m / 60}h` : `${m}m`}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* AQI Forecast Card */}
        <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-lg">
          <h4 className="text-sm font-semibold text-slate-300 mb-3">AQI Forecast Horizon (+{selectedHorizonMinutes}m)</h4>
          <div className="flex items-baseline space-x-4">
            <span className="text-4xl font-extrabold text-orange-400">{currentForecastPoint.predicted_aqi}</span>
            <span className="text-sm text-slate-400">Confidence: {(currentForecastPoint.confidence * 100).toFixed(0)}%</span>
          </div>
        </div>

        {/* Plume Spread Card */}
        <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-lg">
          <h4 className="text-sm font-semibold text-slate-300 mb-3">Plume Propagation Vector</h4>
          <div className="text-sm space-y-1 text-slate-300">
            <p>Center Lat/Lon: {currentPlumeHorizon.center_latitude.toFixed(4)}, {currentPlumeHorizon.center_longitude.toFixed(4)}</p>
            <p>Radius: {currentPlumeHorizon.radius_km} km | Dispersion Intensity: {currentPlumeHorizon.intensity}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
