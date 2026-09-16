import unittest
from datetime import datetime, timezone
from app.models.alert import AlertModel, AlertStatus, VALID_TRANSITIONS
from app.services.authority_service import AuthorityService
from app.response.priority import PriorityEngine
from app.response.recommendations import RecommendationEngine
from app.services.alert_service import AlertService
from app.intelligence.hotspot_detector import HotspotDetectorService
from app.prediction.prediction_service import PredictionService
from app.repositories.observation_repo import InMemoryObservationRepository
from app.repositories.evidence_repo import get_evidence_repository
from app.services.observation_service import ObservationService
from app.models.observation import ObservationCreate, SourceType

class TestPhase5AlertsAndAuthority(unittest.TestCase):
    def setUp(self):
        AlertService.reset_store()
        self.obs_repo = InMemoryObservationRepository()
        self.ev_repo = get_evidence_repository()
        self.obs_service = ObservationService(self.obs_repo)
        
        self.obs_service.create_observation(ObservationCreate(
            timestamp=datetime.now(timezone.utc),
            latitude=28.7041,
            longitude=77.1025,
            source_type=SourceType.SYNTHETIC_DEMO,
            source_id="sensor-1",
            city="Delhi",
            corridor="NH-44 Industrial Freight Artery",
            aqi=380.0,
            pm25=280.0,
            wind_speed_kmh=12.0,
            wind_direction_deg=180.0,
            confidence=0.95,
            data_quality_flag=True
        ))

        self.detector = HotspotDetectorService(self.obs_repo, self.ev_repo)
        self.prediction = PredictionService(self.detector, self.obs_repo)
        self.alert_service = AlertService(self.detector, self.prediction)

    def test_authority_routing(self):
        source, authority, reason = AuthorityService.route_authority(
            likely_source="Industrial Emission",
            corridor="NH-44 Industrial Freight Artery",
            aqi=380.0
        )
        self.assertEqual(authority, "State Pollution Control Board (SPCB)")
        self.assertIn("Industrial", source)

    def test_priority_calculation(self):
        priority = PriorityEngine.calculate_priority(
            aqi=380.0,
            confidence=0.95,
            affected_population=75000,
            corridor_present=True
        )
        self.assertIn("priority_score", priority)
        self.assertIn("priority_level", priority)
        self.assertGreaterEqual(priority["priority_score"], 0.0)

    def test_recommendations(self):
        recs = RecommendationEngine.get_recommendations("Industrial Emission")
        self.assertGreater(len(recs), 0)
        self.assertIn("inspection", recs[0].lower())

    def test_alert_state_persistence_and_transitions(self):
        alerts = self.alert_service.get_all_alerts()
        self.assertGreater(len(alerts), 0)
        alert_id = alerts[0].event_id

        initial_status = alerts[0].status
        self.assertIn(initial_status, [AlertStatus.HIGH_CONFIDENCE, AlertStatus.DETECTED])

        if initial_status == AlertStatus.HIGH_CONFIDENCE:
            updated = self.alert_service.update_alert_status(alert_id, AlertStatus.ROUTED)
            self.assertEqual(updated.status, AlertStatus.ROUTED)

            updated2 = self.alert_service.update_alert_status(alert_id, AlertStatus.ACKNOWLEDGED)
            self.assertEqual(updated2.status, AlertStatus.ACKNOWLEDGED)

        with self.assertRaises(ValueError):
            self.alert_service.update_alert_status(alert_id, AlertStatus.RESOLVED)

if __name__ == "__main__":
    unittest.main()
