from typing import Dict, Any

class PriorityEngine:
    @staticmethod
    def calculate_priority(
        aqi: float,
        confidence: float,
        affected_population: int,
        corridor_present: bool
    ) -> Dict[str, Any]:
        aqi_norm = min(max(aqi / 500.0, 0.0), 1.0)
        conf_norm = min(max(confidence, 0.0), 1.0)
        pop_norm = min(max(affected_population / 200000.0, 0.0), 1.0)
        corr_weight = 1.2 if corridor_present else 1.0

        score = (aqi_norm * 0.4 + conf_norm * 0.3 + pop_norm * 0.3) * corr_weight * 100.0
        score = round(min(max(score, 0.0), 100.0), 2)

        if score >= 75.0:
            level = "CRITICAL"
            severity = "High Severity / Urgent Action"
        elif score >= 50.0:
            level = "HIGH"
            severity = "Elevated Severity / Immediate Review"
        elif score >= 25.0:
            level = "MEDIUM"
            severity = "Moderate Severity / Standard Protocol"
        else:
            level = "LOW"
            severity = "Low Severity / Monitor"

        return {
            "priority_score": score,
            "priority_level": level,
            "severity": severity
        }
