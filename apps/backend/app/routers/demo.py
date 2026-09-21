from fastapi import APIRouter
from app.repositories.observation_repo import get_repository
from app.repositories.evidence_repo import get_evidence_repository
from app.intelligence.hotspot_detector import HotspotDetectorService
from app.prediction.prediction_service import PredictionService
from app.services.alert_service import AlertService
from app.federation.coordinator import FederatedCoordinator

router = APIRouter(prefix="/api/v1/demo", tags=["demo"])

def build_services():
    obs_repo = get_repository()
    evidence_repo = get_evidence_repository()
    detector = HotspotDetectorService(obs_repo, evidence_repo)
    prediction = PredictionService(detector, obs_repo)
    alerts = AlertService(detector, prediction)
    return detector, prediction, alerts

@router.post("/run")
def run_demo():
    detector, _, alerts = build_services()
    hotspots = detector.run_detection()
    round_result = FederatedCoordinator.get_coordinator().run_federation_round()
    return {
        "status": "demo_completed",
        "hotspot_count": len(hotspots),
        "alert_count": len(alerts.get_all_alerts()),
        "federation_round": round_result,
    }

@router.post("/reset")
def reset_demo():
    AlertService.reset_store()
    FederatedCoordinator.reset_coordinator()
    PredictionService.reset_cache()
    detector, _, alerts = build_services()
    hotspots = detector.run_detection()
    coordinator = FederatedCoordinator.get_coordinator()
    return {
        "status": "demo_reset",
        "hotspot_count": len(hotspots),
        "alert_count": len(alerts.get_all_alerts()),
        "federation": coordinator.get_federation_status(),
    }
