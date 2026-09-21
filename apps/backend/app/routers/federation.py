from typing import List
import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.federation.coordinator import FederatedCoordinator
from app.federation.node import FederatedNode

router = APIRouter(prefix="/api/v1/federation", tags=["federation"])

class NodeRegistration(BaseModel):
    node_id: str = Field(min_length=1)
    city: str = Field(min_length=1)
    state: str = Field(min_length=1)
    dataset_size: int = Field(default=150, ge=1)

class PredictionRequest(BaseModel):
    features: List[float] = Field(min_length=7, max_length=7)

@router.get("/status")
def get_status():
    return FederatedCoordinator.get_coordinator().get_federation_status()

@router.get("/nodes")
def get_nodes():
    coordinator = FederatedCoordinator.get_coordinator()
    return [node.get_status_dict() for node in coordinator.get_all_nodes()]

@router.get("/rounds")
def get_rounds():
    return FederatedCoordinator.get_coordinator().round_history

@router.post("/register-node", status_code=201)
def register_node(payload: NodeRegistration):
    coordinator = FederatedCoordinator.get_coordinator()
    if coordinator.get_node(payload.node_id):
        raise HTTPException(status_code=409, detail=f"Node '{payload.node_id}' already registered")
    node = FederatedNode(payload.node_id, payload.city, payload.state, dataset_size=payload.dataset_size)
    coordinator.register_node(node)
    return node.get_status_dict()

@router.post("/round")
def run_round():
    return FederatedCoordinator.get_coordinator().run_federation_round()

@router.post("/predict")
def predict(payload: PredictionRequest):
    coordinator = FederatedCoordinator.get_coordinator()
    prediction = coordinator.global_model.predict(np.array([payload.features]))
    return {
        "predicted_aqi": float(prediction[0]),
        "model_version": coordinator.global_model_version,
        "is_global_model": True,
    }

@router.get("/model/{node_id}")
def get_node_model(node_id: str):
    coordinator = FederatedCoordinator.get_coordinator()
    node = coordinator.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Federation node '{node_id}' not found")
    return node.get_status_dict()
