from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from app.models.alert import AlertModel, AlertStatus, VALID_TRANSITIONS
from app.services.authority_service import AuthorityService
from app.response.priority import PriorityEngine
from app.response.recommendations import RecommendationEngine
from app.intelligence.hotspot_detector import HotspotDetectorService
from app.prediction.prediction_service import PredictionService

class AlertService:
    _shared_alerts_db: Dict[str, AlertModel] = {}
    _initialized: bool = False

    def __init__(self, detector_service: HotspotDetectorService, prediction_service: PredictionService):
        self.detector_service = detector_service
        self.prediction_service = prediction_service
        if not AlertService._initialized:
            self._initialize_default_alerts()
            AlertService._initialized = True

    @classmethod
    def reset_store(cls):
        cls._shared_alerts_db.clear()
        cls._initialized = False

    def _initialize_default_alerts(self):
        hotspots = self.detector_service.run_detection()
        for hs in hotspots:
            forecast = self.prediction_service.get_forecast(hs.hotspot_id)
            exposure = self.prediction_service.get_exposure(hs.hotspot_id)
            
            peak_aqi = max([f["predicted_aqi"] for f in forecast["forecasts"]]) if forecast and "forecasts" in forecast else 350.0
            pop = exposure["estimated_population"] if exposure else 50000
            corridor_name = hs.corridor if hasattr(hs, "corridor") and hs.corridor else f"Regional Corridor ({hs.city})"
            
            source_category, authority, routing_reason = AuthorityService.route_authority(
                likely_source="Industrial Emission" if hs.hotspot_score > 0.7 else "General Urban Smog",
                corridor=corridor_name,
                aqi=peak_aqi
            )
            
            priority_data = PriorityEngine.calculate_priority(
                aqi=peak_aqi,
                confidence=hs.confidence,
                affected_population=pop,
                corridor_present=True
            )
            
            recommendations = RecommendationEngine.get_recommendations(source_category)
            
            event_id = f"EVT-{hs.hotspot_id}"
            alert = AlertModel(
                event_id=event_id,
                hotspot_id=hs.hotspot_id,
                severity=priority_data["severity"],
                priority_score=priority_data["priority_score"],
                priority_level=priority_data["priority_level"],
                location={"lat": hs.latitude, "lon": hs.longitude},
                likely_source=source_category,
                confidence=hs.confidence,
                affected_population=pop,
                corridor=corridor_name,
                predicted_peak=peak_aqi,
                assigned_authority=authority,
                routing_reason=routing_reason,
                status=AlertStatus.HIGH_CONFIDENCE,
                recommended_response=recommendations
            )
            AlertService._shared_alerts_db[event_id] = alert

    def get_all_alerts(self) -> List[AlertModel]:
        return list(AlertService._shared_alerts_db.values())

    def get_alert(self, event_id: str) -> Optional[AlertModel]:
        return AlertService._shared_alerts_db.get(event_id)

    def update_alert_status(self, event_id: str, new_status: AlertStatus) -> Optional[AlertModel]:
        alert = AlertService._shared_alerts_db.get(event_id)
        if not alert:
            return None
        
        current_status = alert.status
        allowed = VALID_TRANSITIONS.get(current_status, [])
        if new_status not in allowed and new_status != current_status:
            raise ValueError(f"Invalid state transition from {current_status} to {new_status}. Allowed: {allowed}")
        
        alert.status = new_status
        alert.updated_at = datetime.now(timezone.utc)
        AlertService._shared_alerts_db[event_id] = alert
        return alert
