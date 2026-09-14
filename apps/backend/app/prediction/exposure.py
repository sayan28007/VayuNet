import math
from typing import Dict, Any

class ExposureEngine:
    """
    Estimates population exposure within plume radius using synthetic density data.
    """
    @staticmethod
    def estimate_exposure(radius_km: float, intensity: float) -> Dict[str, Any]:
        area_km2 = math.pi * (radius_km ** 2)
        # Assume average urban density of ~15,000 people/km2 in impacted corridors
        base_density_per_km2 = 15000
        estimated_population = int(area_km2 * base_density_per_km2 * (0.5 + 0.5 * intensity))
        
        return {
            "estimated_population": estimated_population,
            "area_km2": round(area_km2, 2),
            "confidence": 0.75,
            "data_source": "synthetic_demo"
        }
