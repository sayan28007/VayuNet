interface Props {
  onRunDemo: () => void;
  onResetDemo: () => void;
  loading: boolean;
}

export default function DemoHero({ onRunDemo, onResetDemo, loading }: Props) {
  return (
    <section className="relative overflow-hidden rounded-3xl border border-cyan-900/60 bg-gradient-to-br from-cyan-950 via-slate-900 to-slate-950 p-6 shadow-2xl sm:p-8">
      <div className="absolute -right-20 -top-20 h-56 w-56 rounded-full bg-cyan-500/10 blur-3xl" />
      <div className="absolute -bottom-24 left-1/3 h-48 w-48 rounded-full bg-blue-500/10 blur-3xl" />
      <div className="relative z-10 max-w-4xl">
        <div className="mb-3 inline-flex items-center rounded-full border border-cyan-800 bg-cyan-950/60 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.2em] text-cyan-300">
          Final Hackathon Demo
        </div>
        <h2 className="text-3xl font-black tracking-tight text-white sm:text-5xl">
          From pollution signal to coordinated action.
        </h2>
        <p className="mt-4 max-w-3xl text-sm leading-6 text-slate-300 sm:text-base">
          VayuNet combines hyperlocal evidence, predictive intelligence, authority response,
          grounded Gemini analysis and federated learning in one operational command center.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={onRunDemo}
            disabled={loading}
            className="rounded-xl bg-cyan-500 px-5 py-2.5 text-sm font-bold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Running..." : "Run Demo"}
          </button>
          <button
            type="button"
            onClick={onResetDemo}
            disabled={loading}
            className="rounded-xl border border-slate-700 bg-slate-900/80 px-5 py-2.5 text-sm font-semibold text-slate-200 transition hover:border-slate-600 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Reset Demo
          </button>
        </div>
      </div>
    </section>
  );
}
