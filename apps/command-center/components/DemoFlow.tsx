const steps = [
  ["01", "Signal", "Sensor, citizen and official observations"],
  ["02", "Fusion", "Temporal, spatial and multimodal evidence"],
  ["03", "Prediction", "AQI forecast, plume and exposure"],
  ["04", "Response", "Priority, authority routing and actions"],
  ["05", "Intelligence", "Grounded Gemini explanation"],
  ["06", "Federation", "Cross-city model learning with FedAvg"],
];

export default function DemoFlow() {
  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl">
      <div className="mb-5">
        <h2 className="text-lg font-bold text-white">How the demo works</h2>
        <p className="text-xs text-slate-400">One signal, one operational story.</p>
      </div>
      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-6">
        {steps.map(([number, title, description]) => (
          <div key={number} className="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <div className="text-[10px] font-bold tracking-[0.18em] text-cyan-400">{number}</div>
            <div className="mt-2 text-sm font-bold text-white">{title}</div>
            <div className="mt-2 text-xs leading-5 text-slate-500">{description}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
