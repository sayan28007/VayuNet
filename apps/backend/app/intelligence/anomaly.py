from statistics import mean, pstdev
from typing import List
from app.models.observation import Observation

class AnomalyDetector:
    def score(self, value: float, baseline: List[float]) -> float:
        if len(baseline) < 2:
            return 0.0
        mu=mean(baseline); sd=pstdev(baseline)
        if sd == 0:
            return 0.0
        z=abs((value-mu)/sd)
        return min(1.0, z/3.0)

    def sensor_anomaly_scores(self, observations: List[Observation]) -> List[float]:
        values=[float(o.aqi) for o in observations if o.aqi is not None]
        return [self.score(float(o.aqi), values) if o.aqi is not None else 0.0 for o in observations]
