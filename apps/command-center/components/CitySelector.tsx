"use client";

import { useState } from "react";

type CityOption = {
  name: string;
};

interface Props {
  cities: CityOption[];
  selectedCity: string;
  onSelectCity: (city: string) => void;
  onAddCity: (city: string) => void;
}

export default function CitySelector({ cities, selectedCity, onSelectCity, onAddCity }: Props) {
  const [newCity, setNewCity] = useState("");
  const [open, setOpen] = useState(false);

  const addCity = () => {
    const city = newCity.trim();
    if (!city) return;
    onAddCity(city);
    onSelectCity(city);
    setNewCity("");
    setOpen(false);
  };

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-4 shadow-xl">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wider text-slate-500">City</div>
          <div className="mt-1 text-sm font-semibold text-white">Monitor a specific city</div>
        </div>
        <div className="flex flex-col gap-2 sm:flex-row">
          <select
            value={selectedCity}
            onChange={(event) => onSelectCity(event.target.value)}
            className="rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none"
          >
            <option value="All Cities">All Cities</option>
            {cities.map((city) => (
              <option key={city.name} value={city.name}>{city.name}</option>
            ))}
          </select>
          <button
            type="button"
            onClick={() => setOpen((value) => !value)}
            className="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-500"
          >
            Add City
          </button>
        </div>
      </div>

      {open && (
        <div className="mt-3 flex flex-col gap-2 border-t border-slate-800 pt-3 sm:flex-row">
          <input
            value={newCity}
            onChange={(event) => setNewCity(event.target.value)}
            onKeyDown={(event) => { if (event.key === "Enter") addCity(); }}
            placeholder="Enter city name"
            className="min-w-0 flex-1 rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none"
          />
          <button
            type="button"
            onClick={addCity}
            className="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-500"
          >
            Add
          </button>
        </div>
      )}
    </section>
  );
}
