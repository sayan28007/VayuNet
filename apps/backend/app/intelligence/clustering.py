from typing import List, Sequence
import numpy as np
from sklearn.cluster import DBSCAN
from app.models.observation import Observation

class SpatialClusterer:
    def cluster(self, observations: Sequence[Observation], radius_km: float = 5.0) -> List[List[Observation]]:
        if not observations:
            return []
        coords=np.radians(np.array([[o.latitude,o.longitude] for o in observations], dtype=float))
        eps=radius_km/6371.0
        labels=DBSCAN(eps=eps, min_samples=1, metric="haversine").fit(coords).labels_
        groups={}
        for obs,label in zip(observations,labels):
            groups.setdefault(int(label),[]).append(obs)
        return list(groups.values())
