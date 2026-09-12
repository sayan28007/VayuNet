from fastapi.testclient import TestClient

from main import app


def test_health():
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["services"]["gemini"] in {"configured", "not_configured"}
    assert data["services"]["vertex_ai"] == "not_implemented"
    assert data["services"]["bigquery"] == "not_implemented"
    assert data["services"]["firebase"] == "not_implemented"
    assert data["services"]["federation"] == "not_implemented"
