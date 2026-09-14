from typing import List, Optional, Set
from datetime import datetime, timezone
from fastapi import HTTPException
from app.models.observation import Observation, ObservationCreate
from app.repositories.observation_repo import ObservationRepository
from app.utils.geo import calculate_distance_km, is_within_bbox

class ObservationService:
    def __init__(self, repo: ObservationRepository):
        self.repo = repo

    def create_observation(self, obs_in: ObservationCreate) -> Observation:
        if obs_in.timestamp > datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Timestamp cannot be in the future")
            
        # Duplicate Rule Check: source_id + timestamp + lat + lon
        if self.repo.exists(obs_in.source_id, obs_in.timestamp, obs_in.latitude, obs_in.longitude):
            raise HTTPException(status_code=409, detail="Duplicate observation detected")
            
        # Basic sanity checks handled by Pydantic, apply business data quality rules here
        data_quality = True
        if obs_in.aqi and obs_in.aqi > 500:
            data_quality = False # Flag extreme outliers for review
            
        obs = Observation(
            **obs_in.model_dump(),
            data_quality_flag=data_quality
        )
        return self.repo.save(obs)

    def get_observation(self, obs_id: str) -> Optional[Observation]:
        return self.repo.get_by_id(obs_id)

    def list_observations(
        self, 
        city: Optional[str] = None, 
        corridor: Optional[str] = None,
        min_lat: Optional[float] = None,
        max_lat: Optional[float] = None,
        min_lon: Optional[float] = None,
        max_lon: Optional[float] = None,
        center_lat: Optional[float] = None,
        center_lon: Optional[float] = None,
        radius_km: Optional[float] = None
    ) -> List[Observation]:
        all_obs = self.repo.get_all()
        filtered = []
        
        for obs in all_obs:
            if city and obs.city != city:
                continue
            if corridor and obs.corridor != corridor:
                continue
            if all(v is not None for v in [min_lat, max_lat, min_lon, max_lon]):
                if not is_within_bbox(obs.latitude, obs.longitude, min_lat, max_lat, min_lon, max_lon): # type: ignore
                    continue
            if all(v is not None for v in [center_lat, center_lon, radius_km]):
                dist = calculate_distance_km(obs.latitude, obs.longitude, center_lat, center_lon) # type: ignore
                if dist > radius_km: # type: ignore
                    continue
            filtered.append(obs)
            
        # Sort by latest first
        return sorted(filtered, key=lambda x: x.timestamp, reverse=True)

    def get_cities(self) -> List[str]:
        cities: Set[str] = set()
        for obs in self.repo.get_all():
            if obs.city:
                cities.add(obs.city)
        return sorted(list(cities))

    def get_corridors(self) -> List[str]:
        corridors: Set[str] = set()
        for obs in self.repo.get_all():
            if obs.corridor:
                corridors.add(obs.corridor)
        return sorted(list(corridors))
        
    def derive_hotspots(self) -> List[dict]:
        """
        Rule-based Phase 2 hotspot heuristic based purely on AQI > 150 (Unhealthy).
        This is a simple deterministic calculation, NOT an ML prediction.
        Advanced ML hotspot detection is reserved for Phase 3.
        """
        all_obs = self.repo.get_all()
        hotspots = []
        for obs in all_obs:
            if obs.aqi and obs.aqi > 150:
                hotspots.append({
                    "latitude": obs.latitude,
                    "longitude": obs.longitude,
                    "intensity": obs.aqi,
                    "city": obs.city,
                    "trigger_source": obs.source_type
                })
        return hotspots

