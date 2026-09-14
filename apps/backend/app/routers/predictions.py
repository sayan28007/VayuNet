from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.prediction.prediction_service import PredictionService
from app.intelligence.hotspot_detector import HotspotDetectorService
from app.repositories.observation_repo import get_repository as get_obs_repo
from app.repositories.evidence_repo import get_evidence_repository as get_ev_repo

router = APIRouter(prefix="/api/v1/predictions", tags=["Predictions"])

def get_prediction_service() -> PredictionService:
    detector = HotspotDetectorService(get_obs_repo(), get_ev_repo())
    return PredictionService(detector, get_obs_repo())

@router.get("/plume/{hotspot_id}")
def get_plume_prediction(
    hotspot_id: str,
    service: PredictionService = Depends(get_prediction_service)
):
    result = service.get_plume(hotspot_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Hotspot not found for plume prediction"
        )
    return result

@router.get("/forecast/{hotspot_id}")
def get_aqi_forecast(
    hotspot_id: str,
    service: PredictionService = Depends(get_prediction_service)
):
    result = service.get_forecast(hotspot_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Hotspot not found for AQI forecast"
        )
    return result

@router.get("/corridors", response_model=List[Dict[str, Any]])
def get_corridor_risks(
    service: PredictionService = Depends(get_prediction_service)
):
    return service.get_corridors()

@router.get("/exposure/{hotspot_id}")
def get_population_exposure(
    hotspot_id: str,
    service: PredictionService = Depends(get_prediction_service)
):
    result = service.get_exposure(hotspot_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Hotspot not found for population exposure estimation"
        )
    return result
