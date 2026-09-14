from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.models.observation import Observation, ObservationCreate
from app.repositories.observation_repo import get_repository
from app.services.observation_service import ObservationService

router = APIRouter(prefix="/api/v1/observations", tags=["Observations"])

def get_service() -> ObservationService:
    return ObservationService(get_repository())

@router.post("", response_model=Observation)
def create_observation(obs: ObservationCreate, service: ObservationService = Depends(get_service)):
    return service.create_observation(obs)

@router.get("", response_model=List[Observation])
def get_observations(
    city: Optional[str] = None,
    corridor: Optional[str] = None,
    min_lat: Optional[float] = None,
    max_lat: Optional[float] = None,
    min_lon: Optional[float] = None,
    max_lon: Optional[float] = None,
    center_lat: Optional[float] = None,
    center_lon: Optional[float] = None,
    radius_km: Optional[float] = None,
    service: ObservationService = Depends(get_service),
):
    return service.list_observations(
        city,
        corridor,
        min_lat,
        max_lat,
        min_lon,
        max_lon,
        center_lat,
        center_lon,
        radius_km,
    )

@router.get("/{obs_id}", response_model=Observation)
def get_observation_by_id(obs_id: str, service: ObservationService = Depends(get_service)):
    obs = service.get_observation(obs_id)
    if not obs:
        raise HTTPException(status_code=404, detail="Observation not found")
    return obs
