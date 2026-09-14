from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.models.observation import Observation, ObservationCreate
from app.repositories.observation_repo import get_repository
from app.services.observation_service import ObservationService

router = APIRouter(prefix="/api/v1/observations", tags=["Observations"])

def get_service() -> ObservationService:
    repo = get_repository()
    return ObservationService(repo)

@router.post("", response_model=Observation)
def create_observation(obs: ObservationCreate, service: ObservationService = Depends(get_service)):
    return service.create_observation(obs)

@router.get("", response_model=List[Observation])
def get_observations(
    city: Optional[str] = None,
    corridor: Optional[str] = None,
    min_lat: Optional[float] = Query(None, ge=-90.0, le=90.0),
    max_lat: Optional[float] = Query(None, ge=-90.0, le=90.0),
    min_lon: Optional[float] = Query(None, ge=-180.0, le=180.0),
    max_lon: Optional[float] = Query(None, ge=-180.0, le=180.0),
    center_lat: Optional[float] = Query(None, ge=-90.0, le=90.0),
    center_lon: Optional[float] = Query(None, ge=-180.0, le=180.0),
    radius_km: Optional[float] = Query(None, ge=0.0),
    service: ObservationService = Depends(get_service)
):
    return service.list_observations(
        city=city, 
        corridor=corridor, 
        min_lat=min_lat, 
        max_lat=max_lat, 
        min_lon=min_lon, 
        max_lon=max_lon,
        center_lat=center_lat,
        center_lon=center_lon,
        radius_km=radius_km
    )

@router.get("/{obs_id}", response_model=Observation)
def get_observation_by_id(obs_id: str, service: ObservationService = Depends(get_service)):
    obs = service.get_observation(obs_id)
    if not obs:
        raise HTTPException(status_code=404, detail="Observation not found")
    return obs

