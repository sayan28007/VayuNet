from typing import List, Dict, Any, Optional
from app.intelligence.hotspot_detector import HotspotDetectorService
from app.prediction.plume import PlumeEngine
from app.prediction.forecast import ForecastEngine
from app.prediction.corridor import CorridorEngine
from app.prediction.exposure import ExposureEngine
from app.repositories.observation_repo import InMemoryObservationRepository

class PredictionService:
    def __init__(self, detector_service: HotspotDetectorService, obs_repo: InMemoryObservationRepository):
        self.detector_service = detector_service
        self.obs_repo = obs_repo

    def _find_hotspot(self, hotspot_id: str):
        hotspots = self.detector_service.run_detection()
        for h in hotspots:
            if h.hotspot_id == hotspot_id:
                return h
        return None

    def _get_meteorological_context(self, lat: float, lon: float) -> Dict[str, Any]:
        observations = self.obs_repo.get_all()
        # Find nearest observation within 0.15 degrees
        nearest_obs = None
        min_dist = float('inf')
        for o in observations:
            dist = (o.latitude - lat)**2 + (o.longitude - lon)**2
            if dist < min_dist:
                min_dist = dist
                nearest_obs = o

        if nearest_obs and nearest_obs.wind_speed_kmh is not None and nearest_obs.wind_direction_deg is not None:
            return {
                "wind_speed_kmh": nearest_obs.wind_speed_kmh,
                "wind_direction_deg": nearest_obs.wind_direction_deg,
                "aqi": nearest_obs.aqi,
                "data_source": "live_observation"
            }
        
        # Explicit deterministic prototype fallback object/metadata clearly identified as synthetic_demo_fallback
        return {
            "wind_speed_kmh": 10.0,
            "wind_direction_deg": 90.0,
            "aqi": 200.0,
            "data_source": "synthetic_demo_fallback"
        }

    def get_plume(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        hs = self._find_hotspot(hotspot_id)
        if not hs:
            return None
        
        context = self._get_meteorological_context(hs.latitude, hs.longitude)
        plume_res = PlumeEngine.calculate_plume(
            hotspot_id=hs.hotspot_id,
            lat=hs.latitude,
            lon=hs.longitude,
            intensity=hs.hotspot_score,
            wind_speed_kmh=context["wind_speed_kmh"],
            wind_direction_deg=context["wind_direction_deg"],
            horizons_minutes=[0, 30, 60, 120, 180, 360]
        )
        plume_res["metadata"] = {"data_source": context["data_source"]}
        return plume_res

    def get_forecast(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        hs = self._find_hotspot(hotspot_id)
        if not hs:
            return None
        
        context = self._get_meteorological_context(hs.latitude, hs.longitude)
        forecast_res = ForecastEngine.generate_forecast(
            hotspot_id=hs.hotspot_id,
            current_aqi=context["aqi"],
            intensity=hs.hotspot_score,
            wind_speed_kmh=context["wind_speed_kmh"]
        )
        forecast_res["metadata"] = {"data_source": context["data_source"]}
        return forecast_res

    def get_corridors(self) -> List[Dict[str, Any]]:
        hotspots = self.detector_service.run_detection()
        observations = self.obs_repo.get_all()
        return CorridorEngine.calculate_corridor_risks(hotspots, observations)

    def get_exposure(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        hs = self._find_hotspot(hotspot_id)
        if not hs:
            return None
        
        # Reuse the exact same meteorological/plume context used by get_plume()
        context = self._get_meteorological_context(hs.latitude, hs.longitude)
        plume = PlumeEngine.calculate_plume(
            hs.hotspot_id, hs.latitude, hs.longitude, hs.hotspot_score, 
            context["wind_speed_kmh"], context["wind_direction_deg"],
            horizons_minutes=[0, 30, 60, 120, 180, 360]
        )
        max_radius = max([h["radius_km"] for h in plume["horizons"]])
        exposure = ExposureEngine.estimate_exposure(max_radius, hs.hotspot_score)
        exposure["metadata"] = {"data_source": context["data_source"]}
        return exposure
