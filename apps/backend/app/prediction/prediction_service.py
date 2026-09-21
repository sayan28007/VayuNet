from typing import List, Dict, Any, Optional
from app.intelligence.hotspot_detector import HotspotDetectorService
from app.prediction.plume import PlumeEngine
from app.prediction.forecast import ForecastEngine
from app.prediction.corridor import CorridorEngine
from app.prediction.exposure import ExposureEngine
from app.repositories.observation_repo import InMemoryObservationRepository

class PredictionService:
    _shared_cached_hotspots = None
    _last_detection_time = None

    def __init__(self, detector_service: HotspotDetectorService, obs_repo: InMemoryObservationRepository):
        self.detector_service = detector_service
        self.obs_repo = obs_repo

    @classmethod
    def reset_cache(cls):
        cls._shared_cached_hotspots = None
        cls._last_detection_time = None

    def _get_hotspots(self):
        if PredictionService._shared_cached_hotspots is None:
            PredictionService._shared_cached_hotspots = self.detector_service.run_detection()
        return PredictionService._shared_cached_hotspots

    def _find_hotspot(self, hotspot_id: str):
        return next((h for h in self._get_hotspots() if h.hotspot_id == hotspot_id), None)

    def _get_meteorological_context(self, lat: float, lon: float) -> Dict[str, Any]:
        observations = self.obs_repo.get_all()
        nearest_obs = None
        min_dist = float("inf")
        for observation in observations:
            dist = (observation.latitude - lat) ** 2 + (observation.longitude - lon) ** 2
            if dist < min_dist:
                min_dist = dist
                nearest_obs = observation
        if nearest_obs and nearest_obs.wind_speed_kmh is not None and nearest_obs.wind_direction_deg is not None:
            return {
                "wind_speed_kmh": nearest_obs.wind_speed_kmh,
                "wind_direction_deg": nearest_obs.wind_direction_deg,
                "aqi": nearest_obs.aqi,
                "data_source": "live_observation",
            }
        return {
            "wind_speed_kmh": 10.0,
            "wind_direction_deg": 90.0,
            "aqi": 200.0,
            "data_source": "synthetic_demo_fallback",
        }

    def get_plume(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        hs = self._find_hotspot(hotspot_id)
        if not hs:
            return None
        context = self._get_meteorological_context(hs.latitude, hs.longitude)
        result = PlumeEngine.calculate_plume(
            hotspot_id=hs.hotspot_id,
            lat=hs.latitude,
            lon=hs.longitude,
            intensity=hs.hotspot_score,
            wind_speed_kmh=context["wind_speed_kmh"],
            wind_direction_deg=context["wind_direction_deg"],
            horizons_minutes=[0, 30, 60, 120, 180, 360],
        )
        result["metadata"] = {"data_source": context["data_source"]}
        return result

    def get_forecast(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        hs = self._find_hotspot(hotspot_id)
        if not hs:
            return None
        context = self._get_meteorological_context(hs.latitude, hs.longitude)
        result = ForecastEngine.generate_forecast(
            hotspot_id=hs.hotspot_id,
            current_aqi=context["aqi"],
            intensity=hs.hotspot_score,
            wind_speed_kmh=context["wind_speed_kmh"],
        )
        result["metadata"] = {"data_source": context["data_source"]}
        return result

    def get_corridors(self) -> List[Dict[str, Any]]:
        return CorridorEngine.calculate_corridor_risks(self._get_hotspots(), self.obs_repo.get_all())

    def get_exposure(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        hs = self._find_hotspot(hotspot_id)
        if not hs:
            return None
        plume = self.get_plume(hotspot_id)
        if not plume:
            return None
        max_radius = max(h["radius_km"] for h in plume["horizons"])
        exposure = ExposureEngine.estimate_exposure(max_radius, hs.hotspot_score)
        exposure["metadata"] = plume.get("metadata", {})
        return exposure
