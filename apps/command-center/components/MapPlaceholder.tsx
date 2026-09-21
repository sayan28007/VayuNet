export default function MapPlaceholder() {
  return (
    <section className="flex min-h-[260px] items-center justify-center rounded-2xl border border-dashed border-slate-700 bg-slate-900 p-6 text-center shadow-xl">
      <div>
        <div className="text-sm font-semibold text-slate-300">Operational Geospatial Map</div>
        <p className="mt-2 max-w-md text-xs leading-5 text-slate-500">
          Geospatial map integration is pending configuration. The selected hotspot telemetry remains available in the command center.
        </p>
      </div>
    </section>
  );
}
