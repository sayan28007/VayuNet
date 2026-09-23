from fastapi.testclient import TestClient

from main import app
from app.cloud.bigquery import BigQueryService
from app.cloud.secret_manager import SecretManagerService
from app.cloud.vertex_ai import VertexAIService
from app.cloud.earth_engine import EarthEngineService

client = TestClient(app)


def test_cloud_status_shape(monkeypatch):
    monkeypatch.setattr(BigQueryService, "is_configured", lambda self: False)
    monkeypatch.setattr(SecretManagerService, "get_status", lambda self: {"status": "not_configured", "secret_id": None})
    monkeypatch.setattr(VertexAIService, "get_status", lambda self: {"status": "not_configured", "project_id": None, "location": "global", "model": "gemini-2.5-flash"})
    monkeypatch.setattr(EarthEngineService, "get_status", lambda self: {"status": "not_configured", "project_id": None, "collection": "COPERNICUS/S5P/NRTI/L3_NO2"})

    response = client.get("/api/v1/cloud/status")
    assert response.status_code == 200
    data = response.json()
    assert set(data) == {"bigquery", "secret_manager", "vertex_ai", "earth_engine"}


def test_vertex_generation_rejects_empty_prompt():
    response = client.post("/api/v1/cloud/vertex-ai/generate", json={"prompt": "   "})
    assert response.status_code == 400


def test_secret_manager_does_not_expose_secret_value(monkeypatch):
    monkeypatch.setattr(SecretManagerService, "get_status", lambda self: {"status": "configured", "secret_id": "gemini-api-key"})
    response = client.get("/api/v1/cloud/secret-manager/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "configured"
    assert "secret_value" not in data
