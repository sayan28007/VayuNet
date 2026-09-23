from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_system_health_surface():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["services"]["backend"] == "healthy"
    assert "google_cloud" in data["services"]
    assert "federation" in data["services"]

def test_cloud_status_surface():
    response = client.get("/api/v1/cloud/status")
    assert response.status_code == 200
    data = response.json()
    assert set(data) == {"bigquery", "secret_manager", "vertex_ai", "earth_engine"}

def test_hotspot_surface():
    response = client.get("/api/v1/hotspots")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_alert_surface():
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_federation_surface():
    response = client.get("/api/v1/federation/status")
    assert response.status_code == 200
    data = response.json()
    assert data["registered_nodes"] >= 3
    assert data["healthy_nodes"] >= 0
