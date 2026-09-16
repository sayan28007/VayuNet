"use client";
import React, { useEffect, useState } from "react";
import AICommandCenter from "../components/AICommandCenter";
import AuthorityResponse from "../components/AuthorityResponse";
import api from "../lib/api";

export default function CommandCenterPage() {
  const [apiStatus, setApiStatus] = useState<string>("Connecting...");

  useEffect(() => {
    api.getHealth()
      .then((data) => setApiStatus(data.status ? `Connected (${data.status})` : "Active"))
      .catch(() => setApiStatus("Backend Offline"));
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-white p-6 md:p-10 space-y-8">
      <header className="border-b border-slate-800 pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-black tracking-tight text-cyan-400">VayuNet Command Center</h1>
          <p className="text-xs text-slate-400">Phase 5: Gemini Operational Intelligence & Authority Response</p>
        </div>
        <div className="text-xs bg-slate-900 border border-slate-800 px-3 py-1.5 rounded text-slate-300">
          Status: {apiStatus}
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <AICommandCenter />
        <AuthorityResponse />
      </div>
    </main>
  );
}