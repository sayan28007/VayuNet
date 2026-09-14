import React from 'react';
import { PopulationExposure } from '../types/prediction';

interface Props {
  exposure?: PopulationExposure;
}

export function ExposurePanel({ exposure }: Props) {
  if (!exposure) return <p className="text-slate-500 p-4">Loading exposure estimation...</p>;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4">
      <h3 className="text-lg font-bold text-white">Population Exposure Estimation</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-lg">
          <span className="text-xs text-slate-400 block">Estimated Exposed Population</span>
          <span className="text-3xl font-extrabold text-red-400 mt-1 block">{exposure.estimated_population.toLocaleString()}</span>
        </div>
        <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-lg">
          <span className="text-xs text-slate-400 block">Impact Area</span>
          <span className="text-3xl font-extrabold text-slate-200 mt-1 block">{exposure.area_km2} km²</span>
        </div>
        <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-lg">
          <span className="text-xs text-slate-400 block">Data Source Metadata</span>
          <span className="text-sm font-semibold text-purple-400 mt-2 block uppercase">{exposure.data_source}</span>
        </div>
      </div>
    </div>
  );
}
