"use client";
import React, { useEffect, useState } from "react";
import api from "../lib/api";

export default function FederatedLearningPanel() {
  const [status, setStatus] = useState<any>(null);
  const [nodes, setNodes] = useState<any[]>([]);
  const [rounds, setRounds] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      const s = await api.getFederationStatus();
      const n = await api.getFederationNodes();
      const r = await api.getFederationRounds();
      setStatus(s);
      setNodes(n || []);
      setRounds(r || []);
      setError(null);
    } catch (err) {
      setError("Failed to fetch federation data");
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleTrainRound = async () => {
    setLoading(true);
    try {
      await api.runFederationRound();
      await fetchData();
    } catch (err: any) {
      setError(err?.message || "Training round failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 p-5 rounded-xl border border-slate-800 space-y-6 shadow-xl">
      <div className="flex justify-between items-center border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-base font-bold text-cyan-400">Federated Learning Network</h3>
          <p className="text-xs text-slate-400">Decentralized multi-node AQI intelligence & model aggregation</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={fetchData}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded transition"
          >
            Refresh Status
          </button>
          <button
            onClick={handleTrainRound}
            disabled={loading}
            className="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white text-xs font-semibold rounded transition"
          >
            {loading ? "Training Round..." : "Train Round"}
          </button>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-950/50 border border-red-800 text-red-300 text-xs rounded">
          {error}
        </div>
      )}

      {status && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Global Model</span>
            <span className="text-sm font-bold text-cyan-400">{status.global_model_version}</span>
          </div>
          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Current Round</span>
            <span className="text-sm font-bold text-amber-400">Round {status.current_round}</span>
          </div>
          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Healthy Nodes</span>
            <span className="text-sm font-bold text-emerald-400">{status.healthy_nodes} / {status.registered_nodes}</span>
          </div>
          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Network Status</span>
            <span className={`text-sm font-bold ${status.status === "READY" ? "text-emerald-400" : "text-amber-400"}`}>
              {status.status}
            </span>
          </div>
        </div>
      )}

      <div className="space-y-3">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">Participating Nodes</h4>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 border-b border-slate-800">
              <tr>
                <th className="p-2 font-medium">Node ID</th>
                <th className="p-2 font-medium">City / State</th>
                <th className="p-2 font-medium">Dataset Size</th>
                <th className="p-2 font-medium">Model Version</th>
                <th className="p-2 font-medium">Local Metric (MSE)</th>
                <th className="p-2 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {nodes.length === 0 ? (
                <tr>
                  <td colSpan={6} className="p-3 text-center text-slate-500">No nodes registered.</td>
                </tr>
              ) : (
                nodes.map((node: any) => (
                  <tr key={node.node_id} className="hover:bg-slate-950/50 transition">
                    <td className="p-2 font-mono text-cyan-300">{node.node_id}</td>
                    <td className="p-2 text-slate-200">{node.city}, {node.state}</td>
                    <td className="p-2 text-slate-300">{node.dataset_size} samples</td>
                    <td className="p-2 font-mono text-amber-300">{node.model_version}</td>
                    <td className="p-2 font-mono text-emerald-300">{node.local_metric}</td>
                    <td className="p-2">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                        node.status === "READY" || node.status === "COMPLETED"
                          ? "bg-emerald-950 text-emerald-400 border border-emerald-800"
                          : node.status === "TRAINING"
                          ? "bg-amber-950 text-amber-400 border border-amber-800"
                          : "bg-red-950 text-red-400 border border-red-800"
                      }`}>
                        {node.status}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {rounds.length > 0 && (
        <div className="space-y-2 pt-2 border-t border-slate-800">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">Latest Round Execution Summary</h4>
          <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs space-y-1">
            {(() => {
              const latest = rounds[rounds.length - 1];
              return (
                <>
                  <div className="flex justify-between text-slate-400">
                    <span>Round ID: <strong className="text-white">#{latest.round_id}</strong></span>
                    <span>Global Version: <strong className="text-cyan-400">{latest.global_model_version}</strong></span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>Total Samples Aggregated: <strong className="text-white">{latest.total_samples}</strong></span>
                    <span>Average Training Metric: <strong className="text-emerald-400">{latest.average_metric} MSE</strong></span>
                  </div>
                  <div className="text-slate-400">
                    Successful Nodes: <strong className="text-emerald-300">{latest.successful_nodes.join(", ")}</strong>
                    {latest.failed_nodes.length > 0 && <span className="text-red-400 ml-2">Failed: {latest.failed_nodes.join(", ")}</span>}
                  </div>
                </>
              );
            })()}
          </div>
        </div>
      )}
    </div>
  );
}
