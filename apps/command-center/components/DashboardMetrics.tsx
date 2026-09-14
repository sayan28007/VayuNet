import React from 'react';
import { Observation } from '../types/observation';

interface Props {
  observations: Observation[];
}

export function DashboardMetrics({ observations }: Props) {
  const total = observations.length;
  const uniqueSources = new Set(observations.map(o => o.source_id)).size;
  const latestDate = observations.length > 0 
    ? new Date(Math.max(...observations.map(o => new Date(o.timestamp).getTime()))).toLocaleString()
    : 'No data';

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="p-4 bg-slate-900 border border-slate-800 rounded-lg">
        <h3 className="text-sm text-slate-400">Total Observations</h3>
        <p className="text-3xl font-bold">{total}</p>
      </div>
      <div className="p-4 bg-slate-900 border border-slate-800 rounded-lg">
        <h3 className="text-sm text-slate-400">Active Sources</h3>
        <p className="text-3xl font-bold">{uniqueSources}</p>
      </div>
      <div className="p-4 bg-slate-900 border border-slate-800 rounded-lg">
        <h3 className="text-sm text-slate-400">Latest Sync</h3>
        <p className="text-lg font-bold mt-2">{latestDate}</p>
      </div>
    </div>
  );
}

