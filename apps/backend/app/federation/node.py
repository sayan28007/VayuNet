import numpy as np
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from app.federation.model import FederatedAQIModel

SEED_MAP = {
    "node-delhi": 101,
    "node-visakhapatnam": 202,
    "node-mumbai": 303
}

class FederatedNode:
    def __init__(self, node_id: str, city: str, state: str, dataset_size: int = 150, seed: Optional[int] = None):
        self.node_id = node_id
        self.city = city
        self.state = state
        self.dataset_size = dataset_size
        self.model = FederatedAQIModel(version="global-v1")
        self.status = "READY"
        self.last_training_round = 0
        self.local_metric = 0.0
        self.last_updated = datetime.now(timezone.utc).isoformat()
        resolved_seed = seed if seed is not None else SEED_MAP.get(node_id, 42)
        np.random.seed(resolved_seed)
        self.X_train = np.random.rand(dataset_size, 7) * np.array([150, 300, 80, 15, 90, 45, 24])
        noise = np.random.normal(0, 10, dataset_size)
        self.y_train = (
            self.X_train[:, 0] * 0.6 +
            self.X_train[:, 1] * 0.2 +
            self.X_train[:, 2] * 0.15 +
            noise + 50.0
        )
        self.train_local()

    def train_local(self) -> Dict[str, Any]:
        self.status = "TRAINING"
        try:
            self.model.fit(self.X_train, self.y_train)
            preds = self.model.predict(self.X_train)
            mse = float(np.mean((preds - self.y_train) ** 2))
            self.local_metric = round(mse, 2)
            self.status = "COMPLETED"
            self.last_updated = datetime.now(timezone.utc).isoformat()
            return {
                "node_id": self.node_id,
                "parameters": self.model.get_parameters(),
                "sample_count": self.dataset_size,
                "metric": self.local_metric,
                "status": "SUCCESS"
            }
        except Exception as e:
            self.status = "FAILED"
            self.last_updated = datetime.now(timezone.utc).isoformat()
            return {
                "node_id": self.node_id,
                "parameters": None,
                "sample_count": self.dataset_size,
                "metric": 0.0,
                "status": "FAILED",
                "error": str(e)
            }

    def update_global_model(self, global_params: Dict[str, Any], round_num: int):
        self.model.set_parameters(global_params)
        self.last_training_round = round_num
        self.status = "READY"
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def predict(self, features: list) -> float:
        X = np.array([features])
        pred = self.model.predict(X)
        return float(pred[0])

    def get_status_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "city": self.city,
            "state": self.state,
            "dataset_size": self.dataset_size,
            "model_version": self.model.version,
            "last_training_round": self.last_training_round,
            "local_metric": self.local_metric,
            "status": self.status,
            "last_updated": self.last_updated
        }
