from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.alert import AlertModel, AlertStatus
from app.services.alert_service import AlertService
from app.intelligence.hotspot_detector import HotspotDetectorService
from app.prediction.prediction_service import PredictionService
from app.repositories.observation_repo import get_repository
from app.repositories.evidence_repo import get_evidence_repository

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])

def get_alert_service() -> AlertService:
    obs_repo = get_repository()
    ev_repo = get_evidence_repository()
    detector = HotspotDetectorService(obs_repo, ev_repo)
    prediction = PredictionService(detector, obs_repo)
    return AlertService(detector, prediction)

@router.get("", response_model=List[AlertModel])
def list_alerts(alert_service: AlertService = Depends(get_alert_service)):
    return alert_service.get_all_alerts()

@router.get("/{event_id}", response_model=AlertModel)
def get_alert(event_id: str, alert_service: AlertService = Depends(get_alert_service)):
    alert = alert_service.get_alert(event_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert with event_id '{event_id}' not found")
    return alert

@router.post("/{event_id}/acknowledge", response_model=AlertModel)
def acknowledge_alert(event_id: str, alert_service: AlertService = Depends(get_alert_service)):
    alert = alert_service.get_alert(event_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert with event_id '{event_id}' not found")
    try:
        updated = alert_service.update_alert_status(event_id, AlertStatus.ACKNOWLEDGED)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{event_id}/action", response_model=AlertModel)
def start_alert_action(event_id: str, alert_service: AlertService = Depends(get_alert_service)):
    alert = alert_service.get_alert(event_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert with event_id '{event_id}' not found")
    try:
        updated = alert_service.update_alert_status(event_id, AlertStatus.ACTION_IN_PROGRESS)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{event_id}/resolve", response_model=AlertModel)
def resolve_alert(event_id: str, alert_service: AlertService = Depends(get_alert_service)):
    alert = alert_service.get_alert(event_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alert with event_id '{event_id}' not found")
    try:
        updated = alert_service.update_alert_status(event_id, AlertStatus.RESOLVED)
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
