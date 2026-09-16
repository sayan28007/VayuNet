"use client";
import React, { useState } from "react";
import api from "../lib/api";

export default function AICommandCenter() {
  const [message, setMessage] = useState("");
  const [language, setLanguage] = useState("en");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleChat = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.postAgentChat(message, language);
      setResult(data);
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const suggestedQuestions = [
    "What are the most severe active hotspots?",
    "Where will the plume move?",
    "Which authority should respond?",
    "How many people could be exposed?"
  ];

  return (
    <div className="bg-slate-900 text-white p-6 rounded-xl border border-slate-700 shadow-xl">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
        🤖 VayuNet AI Command Center
      </h2>
      
      <div className="mb-4 flex gap-2 flex-wrap">
        <span className="text-sm text-slate-400 self-center">Language:</span>
        {["en", "hi", "te"].map((lang) => (
          <button
            key={lang}
            type="button"
            onClick={() => setLanguage(lang)}
            className={`px-3 py-1 rounded text-xs font-semibold ${
              language === lang ? "bg-cyan-600 text-white" : "bg-slate-800 text-slate-300"
            }`}
          >
            {lang.toUpperCase()}
          </button>
        ))}
      </div>

      <div className="mb-4 flex gap-2 flex-wrap">
        <span className="text-xs text-slate-400 self-center">Suggested:</span>
        {suggestedQuestions.map((q, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => setMessage(q)}
            className="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs px-2.5 py-1 rounded border border-slate-700"
          >
            {q}
          </button>
        ))}
      </div>

      <form onSubmit={handleChat} className="space-y-3">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask operational intelligence query..."
          className="w-full bg-slate-950 border border-slate-700 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-cyan-500"
          rows={3}
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded-lg text-sm font-semibold transition disabled:opacity-50"
        >
          {loading ? "Reasoning with Tools..." : "Send Query"}
        </button>
      </form>

      {error && <div className="mt-4 p-3 bg-red-900/50 border border-red-700 text-red-200 text-sm rounded">{error}</div>}

      {result && (
        <div className="mt-6 space-y-4 border-t border-slate-800 pt-4">
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-cyan-400 mb-1">Grounded Response</h3>
            <p className="text-sm bg-slate-950 p-4 rounded-lg border border-slate-800 leading-relaxed">{result.answer}</p>
          </div>
          <div className="grid grid-cols-2 gap-4 text-xs">
            <div className="bg-slate-950 p-3 rounded border border-slate-800">
              <span className="font-semibold text-slate-400 block mb-1">Tools Used:</span>
              <div className="flex flex-wrap gap-1">
                {result.tools_used?.map((t: string, i: number) => (
                  <span key={i} className="bg-slate-800 text-cyan-300 px-2 py-0.5 rounded">{t}</span>
                ))}
              </div>
            </div>
            <div className="bg-slate-950 p-3 rounded border border-slate-800">
              <span className="font-semibold text-slate-400 block mb-1">Data Sources:</span>
              <div className="flex flex-wrap gap-1">
                {result.data_sources?.map((s: string, i: number) => (
                  <span key={i} className="bg-slate-800 text-emerald-300 px-2 py-0.5 rounded">{s}</span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
