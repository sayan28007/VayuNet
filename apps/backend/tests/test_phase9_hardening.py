from fastapi.testclient import TestClient
from main import app
from app.services.alert_service import AlertService
from app.federation.coordinator import FederatedCoordinator
from app.prediction.prediction_service import PredictionService

client = TestClient(app)

def setup_function():
    AlertService.reset_store()
    FederatedCoordinator.reset_coordinator()
    PredictionService.reset_cache()

def teardown_function():
    AlertService.reset_store()
    FederatedCoordinator.reset_coordinator()
    PredictionService.reset_cache()

def test_readiness_endpoint():
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["ready"] is True
    assert data["checks"]["repository"] == "ready"

def test_federation_router_is_available():
    response = client.get("/api/v1/federation/status")
    assert response.status_code == 200
    assert response.json()["registered_nodes"] == 3

def test_federation_round_and_prediction():
    round_response = client.post("/api/v1/federation/round")
    assert round_response.status_code == 200
    assert len(round_response.json()["successful_nodes"]) == 3
    prediction = client.post("/api/v1/federation/predict", json={"features": [45, 90, 20, 5, 60, 28, 12]})
    assert prediction.status_code == 200
    assert prediction.json()["is_global_model"] is True

def test_demo_run_and_reset():
    run_response = client.post("/api/v1/demo/run")
    assert run_response.status_code == 200
    assert run_response.json()["status"] == "demo_completed"
    reset_response = client.post("/api/v1/demo/reset")
    assert reset_response.status_code == 200
    assert reset_response.json()["status"] == "demo_reset"

def test_alert_state_machine_can_route_then_acknowledge():
    alerts = client.get("/api/v1/alerts").json()
    assert alerts
    event_id = alerts[0]["event_id"]
    routed = client.post(f"/api/v1/alerts/{event_id}/route")
    assert routed.status_code == 200
    assert routed.json()["status"] == "ROUTED"
    acknowledged = client.post(f"/api/v1/alerts/{event_id}/acknowledge")
    assert acknowledged.status_code == 200
    assert acknowledged.json()["status"] == "ACKNOWLEDGED"

def test_unknown_federation_node_returns_404():
    response = client.get("/api/v1/federation/model/not-a-node")
    assert response.status_code == 404
