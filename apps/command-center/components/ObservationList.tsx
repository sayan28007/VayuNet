import React from 'react';
import { Observation } from '../types/observation';

interface Props {
  observations: Observation[];
}

export function ObservationList({ observations }: Props) {
  if (observations.length === 0) return <p className="text-slate-500">No observations found.</p>;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="border-b border-slate-800 text-slate-400">
            <th className="p-3">Time</th>
            <th className="p-3">City</th>
            <th className="p-3">AQI</th>
            <th className="p-3">Source</th>
            <th className="p-3">Quality</th>
          </tr>
        </thead>
        <tbody>
          {observations.slice(0, 10).map((obs) => (
            <tr key={obs.id} className="border-b border-slate-800/50 hover:bg-slate-800/20">
              <td className="p-3">{new Date(obs.timestamp).toLocaleTimeString()}</td>
              <td className="p-3">{obs.city || 'Unknown'}</td>
              <td className="p-3">
                <span className={`px-2 py-1 rounded text-xs ${obs.aqi && obs.aqi > 150 ? 'bg-red-900/50 text-red-400' : 'bg-green-900/50 text-green-400'}`}>
                  {obs.aqi?.toFixed(0) || 'N/A'}
                </span>
              </td>
              <td className="p-3 text-sm">{obs.source_type}</td>
              <td className="p-3">
                {obs.data_quality_flag ? '✅' : '⚠️'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

