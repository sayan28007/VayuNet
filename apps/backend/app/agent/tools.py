from typing import List, Dict, Any, Optional
from app.repositories.observation_repo import get_repository
from app.repositories.evidence_repo import get_evidence_repository
from app.services.observation_service import ObservationService
from app.intelligence.hotspot_detector import HotspotDetectorService
from app.prediction.prediction_service import PredictionService
from app.services.alert_service import AlertService
from app.models.alert import AlertStatus
from app.federation.coordinator import FederatedCoordinator

class VayuNetTools:
    def __init__(self, detector_service=None, prediction_service=None, alert_service=None, observation_repo=None, obs_repo=None, evidence_repo=None):
        self.obs_repo = observation_repo or obs_repo or get_repository()
        self.evidence_repo = evidence_repo or get_evidence_repository()
        self.obs_service = ObservationService(self.obs_repo)
        self.hotspot_detector = detector_service or HotspotDetectorService(self.obs_repo, self.evidence_repo)
        self.prediction_service = prediction_service or PredictionService(self.hotspot_detector, self.obs_repo)
        self.alert_service = alert_service or AlertService(self.hotspot_detector, self.prediction_service)
        self.federation_coordinator = FederatedCoordinator.get_coordinator()

    def get_active_hotspots(self) -> List[Dict[str, Any]]:
        hotspots = self.hotspot_detector.run_detection()
        return [hs.dict() if hasattr(hs, "dict") else hs.__dict__ for hs in hotspots]

    def get_hotspot_details(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        return next((hs for hs in self.get_active_hotspots() if hs.get("hotspot_id") == hotspot_id or hs.get("id") == hotspot_id), None)

    def get_forecast(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        return self.prediction_service.get_forecast(hotspot_id)

    def get_plume(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        return self.prediction_service.get_plume(hotspot_id)

    def get_corridor_forecasts(self) -> List[Dict[str, Any]]:
        return self.prediction_service.get_corridors()

    def get_population_exposure(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        return self.prediction_service.get_exposure(hotspot_id)

    def get_active_alerts(self) -> List[Dict[str, Any]]:
        alerts = self.alert_service.get_all_alerts()
        return [a.dict() if hasattr(a, "dict") else a.__dict__ for a in alerts]

    def get_authority_status(self) -> List[Dict[str, Any]]:
        alerts = self.alert_service.get_all_alerts()
        authorities = sorted({a.assigned_authority for a in alerts})
        return [
            {
                "authority": authority,
                "status": "active_routing_ready",
                "active_incidents": sum(1 for a in alerts if a.assigned_authority == authority and a.status != AlertStatus.RESOLVED),
            }
            for authority in authorities
        ]

    def get_response_recommendation(self, incident_type: str) -> Dict[str, Any]:
        for alert in self.alert_service.get_all_alerts():
            if alert.event_id == incident_type or alert.hotspot_id == incident_type or alert.likely_source.lower() == incident_type.lower():
                return {"incident_type": incident_type, "recommendation": alert.recommended_response}
        return {"incident_type": incident_type, "recommendation": ["Follow standard operating protocol"]}

    def get_federated_status(self) -> Dict[str, Any]:
        return self.federation_coordinator.get_federation_status()

    def get_model_version(self) -> str:
        return self.federation_coordinator.global_model_version
