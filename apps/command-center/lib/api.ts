const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = {
  async getHealth() {
    const res = await fetch(`${API_BASE}/api/v1/health`);
    if (!res.ok) throw new Error("Health check failed");
    return res.json();
  },

  async getObservations() {
    const res = await fetch(`${API_BASE}/api/v1/observations`);
    if (!res.ok) throw new Error("Failed to fetch observations");
    return res.json();
  },

  async getCities() {
    const res = await fetch(`${API_BASE}/api/v1/geospatial/cities`);
    if (!res.ok) throw new Error("Failed to fetch cities");
    return res.json();
  },

  async getHotspots() {
    const res = await fetch(`${API_BASE}/api/v1/hotspots`);
    if (!res.ok) throw new Error("Failed to fetch hotspots");
    return res.json();
  },

  async getPlume(hotspotId: string) {
    const res = await fetch(`${API_BASE}/api/v1/predictions/plume/${hotspotId}`);
    if (!res.ok) throw new Error("Failed to fetch plume");
    return res.json();
  },

  async getForecast(hotspotId: string) {
    const res = await fetch(`${API_BASE}/api/v1/predictions/forecast/${hotspotId}`);
    if (!res.ok) throw new Error("Failed to fetch forecast");
    return res.json();
  },

  async getCorridors() {
    const res = await fetch(`${API_BASE}/api/v1/geospatial/corridors`);
    if (!res.ok) throw new Error("Failed to fetch corridors");
    return res.json();
  },

  async getExposure(hotspotId: string) {
    const res = await fetch(`${API_BASE}/api/v1/predictions/exposure/${hotspotId}`);
    if (!res.ok) throw new Error("Failed to fetch exposure");
    return res.json();
  },

  async postAgentChat(message: string, language: string = "en") {
    const res = await fetch(`${API_BASE}/api/v1/agent/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, language }),
    });
    if (!res.ok) throw new Error("Agent chat failed");
    return res.json();
  },

  async getAlerts() {
    const res = await fetch(`${API_BASE}/api/v1/alerts`);
    if (!res.ok) throw new Error("Failed to fetch alerts");
    return res.json();
  },

  async getAlert(eventId: string) {
    const res = await fetch(`${API_BASE}/api/v1/alerts/${eventId}`);
    if (!res.ok) throw new Error("Failed to fetch alert");
    return res.json();
  },

  async acknowledgeAlert(eventId: string) {
    const res = await fetch(`${API_BASE}/api/v1/alerts/${eventId}/acknowledge`, { method: "POST" });
    if (!res.ok) throw new Error("Failed to acknowledge alert");
    return res.json();
  },

  async startAlertAction(eventId: string) {
    const res = await fetch(`${API_BASE}/api/v1/alerts/${eventId}/action`, { method: "POST" });
    if (!res.ok) throw new Error("Failed to start alert action");
    return res.json();
  },

  async resolveAlert(eventId: string) {
    const res = await fetch(`${API_BASE}/api/v1/alerts/${eventId}/resolve`, { method: "POST" });
    if (!res.ok) throw new Error("Failed to resolve alert");
    return res.json();
  },

  async getFederationStatus() {
    const res = await fetch(`${API_BASE}/api/v1/federation/status`);
    if (!res.ok) throw new Error("Failed to fetch federation status");
    return res.json();
  },

  async getFederationNodes() {
    const res = await fetch(`${API_BASE}/api/v1/federation/nodes`);
    if (!res.ok) throw new Error("Failed to fetch federation nodes");
    return res.json();
  },

  async getFederationRounds() {
    const res = await fetch(`${API_BASE}/api/v1/federation/rounds`);
    if (!res.ok) throw new Error("Failed to fetch federation rounds");
    return res.json();
  },

  async runFederationRound() {
    const res = await fetch(`${API_BASE}/api/v1/federation/round`, { method: "POST" });
    if (!res.ok) throw new Error("Failed to execute federation round");
    return res.json();
  }
};

export default api;
