from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

class ForecastEngine:
    """
    Deterministic baseline time-series forecasting for AQI and pollutants.
    """
    @staticmethod
    def generate_forecast(
        hotspot_id: str,
        current_aqi: float,
        intensity: float,
        wind_speed: float
    ) -> Dict[str, Any]:
        horizons = [30, 60, 120, 180, 360] # minutes
        forecast_points = []
        
        # Dispersion decay factor based on wind speed
        decay_rate = 0.05 * (wind_speed / 5.0)
        
        for mins in horizon := horizons:
            hours = mins / 60.0
            # AQI trends toward baseline or decays depending on wind and intensity
            projected_aqi = current_aqi * (1.0 + (intensity * 0.1) - (decay_rate * hours))
            projected_aqi = max(20.0, min(500.0, projected_aqi))
            
            confidence = max(0.5, 0.95 - (mins / 600.0))
            
            forecast_points.append({
                "horizon_minutes": mins,
                "predicted_aqi": round(projected_aqi, 1),
                "confidence": round(confidence, 2)
            })

        return {
            "hotspot_id": hotspot_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "model_name": "deterministic_baseline_v1",
            "forecasts": forecast_points
        }
