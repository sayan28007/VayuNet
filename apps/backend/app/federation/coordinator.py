import numpy as np
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.federation.node import FederatedNode
from app.federation.model import FederatedAQIModel
from app.federation.aggregation import aggregate_fed_avg

class FederatedCoordinator:
    _instance = None

    def __init__(self):
        self.nodes: Dict[str, FederatedNode] = {}
        self.current_round = 0
        self.global_model_version = "global-v1"
        self.global_model = FederatedAQIModel(version="global-v1")
        self.round_history: List[Dict[str, Any]] = []
        self.status = "READY"
        self.last_updated = datetime.now(timezone.utc).isoformat()
        self.register_node(FederatedNode("node-delhi", "Delhi", "Delhi", dataset_size=200))
        self.register_node(FederatedNode("node-visakhapatnam", "Visakhapatnam", "Andhra Pradesh", dataset_size=150))
        self.register_node(FederatedNode("node-mumbai", "Mumbai", "Maharashtra", dataset_size=180))

    @classmethod
    def get_coordinator(cls):
        if cls._instance is None:
            cls._instance = FederatedCoordinator()
        return cls._instance

    @classmethod
    def reset_coordinator(cls):
        cls._instance = None

    def register_node(self, node: FederatedNode):
        self.nodes[node.node_id] = node
        self.last_updated = datetime.now(timezone.utc).isoformat()

    def get_node(self, node_id: str) -> Optional[FederatedNode]:
        return self.nodes.get(node_id)

    def get_all_nodes(self) -> List[FederatedNode]:
        return list(self.nodes.values())

    def run_federation_round(self) -> Dict[str, Any]:
        self.status = "TRAINING"
        self.current_round += 1
        round_id = self.current_round
        participating_nodes = list(self.nodes.keys())
        successful_nodes = []
        failed_nodes = []
        node_results = {}
        for node_id, node in self.nodes.items():
            res = node.train_local()
            node_results[node_id] = res
            if res["status"] == "SUCCESS":
                successful_nodes.append(node_id)
            else:
                failed_nodes.append(node_id)
        timestamp = datetime.now(timezone.utc).isoformat()
        try:
            global_coef, global_intercept, total_samples, successful_nodes = aggregate_fed_avg(node_results)
            self.global_model_version = f"global-v{round_id + 1}"
            global_params = {
                "coef": global_coef.tolist(),
                "intercept": float(global_intercept),
                "version": self.global_model_version,
                "is_fitted": True
            }
            self.global_model.set_parameters(global_params)
            total_metric = 0.0
            for node_id in successful_nodes:
                self.nodes[node_id].update_global_model(global_params, round_id)
                total_metric += node_results[node_id]["metric"] * node_results[node_id]["sample_count"]
            avg_metric = total_metric / total_samples if total_samples > 0 else 0.0
            aggregation_result = {
                "global_coef": global_coef.tolist(),
                "global_intercept": float(global_intercept),
                "aggregation_method": "FedAvg (weighted average)"
            }
            self.status = "READY"
        except Exception as e:
            total_samples = 0
            avg_metric = 0.0
            aggregation_result = {"error": str(e)}
            self.status = "FAILED"
            if not successful_nodes:
                self.current_round -= 1
        self.last_updated = timestamp
        round_summary = {
            "round_id": round_id if self.status != "FAILED" or successful_nodes else self.current_round,
            "participating_nodes": participating_nodes,
            "successful_nodes": successful_nodes,
            "failed_nodes": failed_nodes,
            "node_results": node_results,
            "aggregation_result": aggregation_result,
            "global_model_version": self.global_model_version,
            "total_samples": total_samples,
            "average_metric": round(avg_metric, 2),
            "timestamp": timestamp
        }
        if successful_nodes or self.status != "FAILED":
            self.round_history.append(round_summary)
        return round_summary

    def get_federation_status(self) -> Dict[str, Any]:
        healthy_count = sum(1 for n in self.nodes.values() if n.status in ["READY", "COMPLETED"])
        last_round_time = self.round_history[-1]["timestamp"] if self.round_history else None
        return {
            "status": self.status,
            "global_model_version": self.global_model_version,
            "current_round": self.current_round,
            "registered_nodes": len(self.nodes),
            "healthy_nodes": healthy_count,
            "last_round": last_round_time,
            "last_updated": self.last_updated
        }
