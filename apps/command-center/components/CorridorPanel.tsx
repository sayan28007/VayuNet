import React from 'react';
import { CorridorRisk } from '../types/prediction';

interface Props {
  corridors: CorridorRisk[];
}

export function CorridorPanel({ corridors }: Props) {
  if (corridors.length === 0) return <p className="text-slate-500 p-4">No corridor risk data available.</p>;

  const getRiskColor = (risk: string) => {
    switch(risk) {
      case 'critical': return 'bg-red-900/50 text-red-400 border-red-500';
      case 'high': return 'bg-orange-900/50 text-orange-400 border-orange-500';
      case 'moderate': return 'bg-yellow-900/50 text-yellow-400 border-yellow-500';
      default: return 'bg-slate-800 text-slate-400 border-slate-600';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4">
      <h3 className="text-lg font-bold text-white">Economic Corridor Risk Intelligence</h3>
      <div className="space-y-3">
        {corridors.map((c, idx) => (
          <div key={idx} className="p-4 bg-slate-950/60 border border-slate-800 rounded-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <div className="flex items-center space-x-3 mb-1">
                <h4 className="font-semibold text-white">{c.corridor_name}</h4>
                <span className={`px-2 py-0.5 text-xs font-bold uppercase rounded border ${getRiskColor(c.risk_level)}`}>
                  {c.risk_level}
                </span>
              </div>
              <p className="text-xs text-slate-400">Peak AQI: {c.predicted_peak_aqi} expected in {c.time_to_peak_minutes}m</p>
            </div>
            <div className="flex space-x-6 text-sm">
              <div>
                <span className="text-slate-500 block text-xs">Current AQI</span>
                <span className="font-bold text-slate-200">{c.current_aqi}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-xs">Predicted +1h</span>
                <span className="font-bold text-orange-400">{c.predicted_aqi_1h}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-xs">Confidence</span>
                <span className="font-bold text-slate-300">{(c.confidence * 100).toFixed(0)}%</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
