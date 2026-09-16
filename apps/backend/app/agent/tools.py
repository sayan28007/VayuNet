from typing import List, Dict, Any, Optional
from app.intelligence.hotspot_detector import HotspotDetectorService
from app.prediction.prediction_service import PredictionService
from app.services.alert_service import AlertService
from app.repositories.observation_repo import InMemoryObservationRepository

class VayuNetTools:
    def __init__(
        self,
        detector_service: HotspotDetectorService,
        prediction_service: PredictionService,
        alert_service: AlertService,
        observation_repo: InMemoryObservationRepository
    ):
        self.detector_service = detector_service
        self.prediction_service = prediction_service
        self.alert_service = alert_service
        self.observation_repo = observation_repo

    def get_active_hotspots(self) -> List[Dict[str, Any]]:
        hotspots = self.detector_service.run_detection()
        result = []
        for hs in hotspots:
            result.append({
                "hotspot_id": hs.hotspot_id,
                "city": hs.city,
                "corridor": hs.corridor if hasattr(hs, "corridor") else None,
                "latitude": hs.latitude,
                "longitude": hs.longitude,
                "hotspot_score": hs.hotspot_score,
                "confidence": hs.confidence,
                "timestamp": hs.timestamp.isoformat() if hs.timestamp else None
            })
        return result

    def get_hotspot_details(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        hotspots = self.detector_service.run_detection()
        for hs in hotspots:
            if hs.hotspot_id == hotspot_id:
                forecast = self.prediction_service.get_forecast(hotspot_id)
                exposure = self.prediction_service.get_exposure(hotspot_id)
                return {
                    "hotspot_id": hs.hotspot_id,
                    "city": hs.city,
                    "corridor": hs.corridor if hasattr(hs, "corridor") else None,
                    "latitude": hs.latitude,
                    "longitude": hs.longitude,
                    "hotspot_score": hs.hotspot_score,
                    "confidence": hs.confidence,
                    "forecast": forecast,
                    "exposure": exposure
                }
        return None

    def get_forecast(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        return self.prediction_service.get_forecast(hotspot_id)

    def get_plume(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        return self.prediction_service.get_plume(hotspot_id)

    def get_corridor_forecasts(self) -> List[Dict[str, Any]]:
        hotspots = self.detector_service.run_detection()
        corridors_dict = {}
        for hs in hotspots:
            corr = hs.corridor if hasattr(hs, "corridor") and hs.corridor else f"Corridor-{hs.city}"
            if corr not in corridors_dict:
                corridors_dict[corr] = {
                    "corridor": corr,
                    "city": hs.city,
                    "hotspot_count": 0,
                    "max_score": 0.0
                }
            corridors_dict[corr]["hotspot_count"] += 1
            if hs.hotspot_score > corridors_dict[corr]["max_score"]:
                corridors_dict[corr]["max_score"] = hs.hotspot_score
        return list(corridors_dict.values())

    def get_population_exposure(self, hotspot_id: str) -> Optional[Dict[str, Any]]:
        return self.prediction_service.get_exposure(hotspot_id)

    def get_active_alerts(self) -> List[Dict[str, Any]]:
        alerts = self.alert_service.get_all_alerts()
        return [
            {
                "event_id": a.event_id,
                "hotspot_id": a.hotspot_id,
                "severity": a.severity,
                "priority_level": a.priority_level,
                "likely_source": a.likely_source,
                "assigned_authority": a.assigned_authority,
                "status": a.status,
                "affected_population": a.affected_population,
                "corridor": a.corridor,
                "predicted_peak": a.predicted_peak
            }
            for a in alerts
        ]

    def get_authority_status(self) -> List[Dict[str, Any]]:
        alerts = self.alert_service.get_all_alerts()
        authorities = set(a.assigned_authority for a in alerts)
        return [
            {
                "authority": auth,
                "status": "active_routing_ready",
                "active_incidents": sum(1 for a in alerts if a.assigned_authority == auth)
            }
            for auth in authorities
        ]

    def get_response_recommendation(self, identifier: str) -> Optional[List[str]]:
        alerts = self.alert_service.get_all_alerts()
        for a in alerts:
            if a.event_id == identifier or a.hotspot_id == identifier or a.likely_source.lower() == identifier.lower():
                return a.recommended_response
        return ["Conduct regional field inspection", "Verify stationary sensor telemetry"]

    def get_federated_status(self) -> Dict[str, Any]:
        return {
            "status": "not_implemented",
            "message": "Federated learning synchronization is not implemented in Phase 5. Scheduled for Phase 6.",
            "version": "5.0.0"
        }

    def get_model_version(self) -> Dict[str, Any]:
        return {
            "version": "5.0.0",
            "components": ["HotspotDetector", "PredictionService", "GeminiAgent", "AuthorityService"]
        }
