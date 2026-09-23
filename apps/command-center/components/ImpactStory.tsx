const impactPoints = [
  ["Detect earlier", "Combine diverse signals instead of relying on a single data source."],
  ["Predict next", "Estimate how pollution can move and how exposure can change over time."],
  ["Route action", "Translate incident evidence into priority, authority and response steps."],
  ["Learn together", "Share model updates across simulated city nodes without centralizing local training data."],
];

export default function ImpactStory() {
  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl">
      <div className="mb-5">
        <h2 className="text-lg font-bold text-white">Why VayuNet matters</h2>
        <p className="text-xs text-slate-400">Designed around the operational problem, not a decorative dashboard.</p>
      </div>
      <div className="grid gap-3 md:grid-cols-2">
        {impactPoints.map(([title, body]) => (
          <div key={title} className="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <div className="text-sm font-bold text-cyan-300">{title}</div>
            <p className="mt-2 text-xs leading-5 text-slate-400">{body}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
