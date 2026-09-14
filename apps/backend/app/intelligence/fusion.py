from typing import Dict, List

class FusionEngine:
    def combine(self, anomaly_score: float, density_score: float, source_diversity: float, citizen: bool, image: bool, data_quality: float) -> Dict:
        score=(0.50*anomaly_score)+(0.20*density_score)+(0.20*source_diversity)+(0.15 if citizen else 0)+(0.20 if image else 0)
        score=max(0.0,min(1.0,score))
        score*=max(0.0,min(1.0,data_quality))
        if score >= 0.80: severity="critical"
        elif score >= 0.60: severity="high"
        elif score >= 0.40: severity="moderate"
        else: severity="low"
        return {"score":score,"confidence":score,"severity":severity}
