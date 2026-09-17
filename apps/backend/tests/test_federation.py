import pytest
from fastapi.testclient import TestClient
from main import app
from app.federation.coordinator import FederatedCoordinator

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_federation():
    FederatedCoordinator.reset_coordinator()
    yield
    FederatedCoordinator.reset_coordinator()

def test_get_federation_status():
    response = client.get("/api/v1/federation/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "READY"
    assert data["registered_nodes"] == 3
    assert data["current_round"] == 0

def test_get_nodes():
    response = client.get("/api/v1/federation/nodes")
    assert response.status_code == 200
    nodes = response.json()
    assert len(nodes) == 3
    node_ids = [n["node_id"] for n in nodes]
    assert "node-delhi" in node_ids
    assert "node-visakhapatnam" in node_ids
    assert "node-mumbai" in node_ids

def test_register_node():
    payload = {
        "node_id": "node-bengaluru",
        "city": "Bengaluru",
        "state": "Karnataka",
        "dataset_size": 120
    }
    response = client.post("/api/v1/federation/register-node", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["node_id"] == "node-bengaluru"
    assert data["city"] == "Bengaluru"
    
    status_res = client.get("/api/v1/federation/status")
    assert status_res.json()["registered_nodes"] == 4

def test_execute_federated_round():
    response = client.post("/api/v1/federation/round")
    assert response.status_code == 200
    data = response.json()
    assert data["round_id"] == 1
    assert len(data["successful_nodes"]) == 3
    
    status_res = client.get("/api/v1/federation/status")
    assert status_res.json()["current_round"] == 1

def test_model_prediction():
    client.post("/api/v1/federation/round")
    
    predict_payload = {
        "features": [45.0, 90.0, 20.0, 5.0, 60.0, 28.0, 12.0]
    }
    response = client.post("/api/v1/federation/predict", json=predict_payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_aqi" in data
    assert data["is_global_model"] is True

def test_node_not_found():
    response = client.get("/api/v1/federation/model/non-existent-node")
    assert response.status_code == 404
