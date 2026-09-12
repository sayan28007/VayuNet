'use client';

import { useEffect, useState } from "react";
import { config } from '@/lib/config';

type HealthResponse = {
  status: string;
};

export default function Dashboard() {
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    fetch(`${config.apiBaseUrl}/api/v1/health`)
      .then((res) => res.json())
      .then((data: HealthResponse) => setHealth(data))
      .catch(() => setHealth(null));
  }, []);

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold">VayuNet Command Center</h1>
      <p className="mt-4">
        Backend Status: {health?.status || "Connecting..."}
      </p>
    </main>
  );
}
