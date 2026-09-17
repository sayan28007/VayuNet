import numpy as np
from typing import List, Dict, Any, Tuple

def aggregate_fed_avg(node_results: Dict[str, Dict[str, Any]]) -> Tuple[np.ndarray, float, int, List[str]]:
    """
    Performs weighted Federated Averaging (FedAvg) on successful node training updates.
    """
    total_samples = 0
    accumulated_coef = None
    accumulated_intercept = 0.0
    successful_nodes = []

    for node_id, res in node_results.items():
        if res.get("status") == "SUCCESS" and res.get("parameters") is not None:
            successful_nodes.append(node_id)
            sample_count = res["sample_count"]
            total_samples += sample_count
            params = res["parameters"]
            coef = np.array(params["coef"])
            intercept = params["intercept"]
            if accumulated_coef is None:
                accumulated_coef = coef * sample_count
            else:
                accumulated_coef += coef * sample_count
            accumulated_intercept += intercept * sample_count

    if total_samples > 0 and accumulated_coef is not None:
        global_coef = accumulated_coef / total_samples
        global_intercept = accumulated_intercept / total_samples
        return global_coef, float(global_intercept), total_samples, successful_nodes

    raise ValueError("No valid node updates available for aggregation.")
