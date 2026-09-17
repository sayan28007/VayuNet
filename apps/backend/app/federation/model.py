import numpy as np
from sklearn.linear_model import Ridge
from typing import Dict, Any

class FederatedAQIModel:
    def __init__(self, version: str = "global-v1"):
        self.version = version
        self.model = Ridge(alpha=1.0)
        self.is_fitted = False
        self.feature_dim = 7

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.model.fit(X, y)
        self.is_fitted = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            return np.full((X.shape[0],), 100.0)
        return self.model.predict(X)

    def get_parameters(self) -> Dict[str, Any]:
        if not self.is_fitted:
            return {
                "coef": [0.0] * self.feature_dim,
                "intercept": 100.0,
                "version": self.version,
                "is_fitted": False
            }
        return {
            "coef": self.model.coef_.tolist(),
            "intercept": float(self.model.intercept_),
            "version": self.version,
            "is_fitted": True
        }

    def set_parameters(self, params: Dict[str, Any]):
        self.version = params.get("version", self.version)
        coef = params.get("coef")
        intercept = params.get("intercept")
        is_fitted = params.get("is_fitted", True)
        if coef is not None and intercept is not None:
            self.model.coef_ = np.array(coef)
            self.model.intercept_ = float(intercept)
            self.model.n_features_in_ = len(coef)
            self.is_fitted = is_fitted
