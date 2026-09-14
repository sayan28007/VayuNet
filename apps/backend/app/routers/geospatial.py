from fastapi import APIRouter, Depends
from typing import List
from app.repositories.observation_repo import get_repository
from app.services.observation_service import ObservationService

router = APIRouter(prefix="/api/v1", tags=["Geospatial"])

def get_service() -> ObservationService:
    return ObservationService(get_repository())

@router.get("/cities", response_model=List[str])
def get_cities(service: ObservationService = Depends(get_service)):
    return service.get_cities()

@router.get("/corridors", response_model=List[str])
def get_corridors(service: ObservationService = Depends(get_service)):
    return service.get_corridors()

@router.get("/hotspots", response_model=List[dict])
def get_hotspots(service: ObservationService = Depends(get_service)):
    return service.derive_hotspots()

