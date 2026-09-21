"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import type { AgentChatResponse } from "@/types/api";

export default function GeminiPanel() {
  const [message, setMessage] = useState("");
  const [language, setLanguage] = useState("en");
  const [result, setResult] = useState<AgentChatResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async () => {
    if (!message.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.chatWithAgent(message.trim(), language);
      setResult(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Agent request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-5 shadow-xl">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div><h2 className="text-lg font-bold text-white">Gemini Intelligence</h2><p className="text-xs text-slate-400">Grounded operational analyst</p></div>
        <div className="flex gap-2">
          {["en", "hi", "te"].map((lang) => <button key={lang} type="button" onClick={() => setLanguage(lang)} className={`rounded-lg px-2.5 py-1 text-xs font-semibold ${language === lang ? "bg-cyan-600 text-white" : "bg-slate-800 text-slate-300"}`}>{lang.toUpperCase()}</button>)}
        </div>
      </div>
      <div className="mt-4 flex gap-2">
        <input value={message} onChange={(e) => setMessage(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter") submit(); }} placeholder="Ask analyst..." className="min-w-0 flex-1 rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-white outline-none" />
        <button type="button" onClick={submit} disabled={loading} className="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50">{loading ? "..." : "Ask"}</button>
      </div>
      {error && <div className="mt-3 text-sm text-amber-300">{error}</div>}
      {result && <div className="mt-4 rounded-xl bg-slate-950 p-4 text-sm text-slate-200"><div>{result.answer}</div><div className="mt-3 text-xs text-slate-500">Tools: {result.tools_used.length ? result.tools_used.join(", ") : "none"}</div></div>}
    </section>
  );
}
