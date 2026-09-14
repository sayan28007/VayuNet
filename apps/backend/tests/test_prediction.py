import unittest
from datetime import datetime, timezone
from app.models.observation import ObservationCreate, SourceType
from app.repositories.observation_repo import InMemoryObservationRepository
from app.repositories.evidence_repo import EvidenceRepository
from app.intelligence.hotspot_detector import HotspotDetectorService
from app.prediction.prediction_service import PredictionService
from app.prediction.plume import PlumeEngine
from app.prediction.forecast import ForecastEngine
from app.prediction.corridor import CorridorEngine
from app.prediction.exposure import ExposureEngine

class TestPhase4FinalCompatibility(unittest.TestCase):
    def setUp(self):
        # Use concrete implementations as requested
        self.obs_repo = InMemoryObservationRepository()
        self.ev_repo = EvidenceRepository()
        
        # Test Phase 2 SourceType compatibility
        obs = self.obs_repo.add(ObservationCreate(
            timestamp=datetime.now(timezone.utc),
            latitude=28.7041,
            longitude=77.1025,
            source_type=SourceType.OFFICIAL_MONITOR,
            source_id="monitor-delhi-1",
            city="Delhi",
            corridor="NH-44 Industrial Freight Artery",
            aqi=320.0,
            pm25=220.0,
            wind_speed_kmh=15.0,
            wind_direction_deg=180.0,
            confidence=0.98,
            data_quality_flag=True
        ))
        
        self.detector = HotspotDetectorService(self.obs_repo, self.ev_repo)
        self.service = PredictionService(self.detector, self.obs_repo)

    def test_sourcetype_compatibility(self):
        st = SourceType.CITIZEN_REPORT
        self.assertEqual(st, "citizen_report")
        st2 = SourceType.OFFICIAL_MONITOR
        self.assertEqual(st2, "official_monitor")

    def test_dynamic_wind_and_aqi_extraction(self):
        hotspots = self.detector.run_detection()
        self.assertGreater(len(hotspots), 0)
        hs_id = hotspots[0].hotspot_id
        
        plume = self.service.get_plume(hs_id)
        self.assertIsNotNone(plume)
        self.assertEqual(plume["metadata"]["data_source"], "live_observation")
        
        forecast = self.service.get_forecast(hs_id)
        self.assertIsNotNone(forecast)
        # Verify 5 forecast horizons
        self.assertEqual(len(forecast["forecasts"]), 5)
        expected_forecast_horizons = [30, 60, 120, 180, 360]
        for idx, pt in enumerate(forecast["forecasts"]):
            self.assertEqual(pt["horizon_minutes"], expected_forecast_horizons[idx])

    def test_plume_horizons(self):
        hotspots = self.detector.run_detection()
        hs_id = hotspots[0].hotspot_id
        plume = self.service.get_plume(hs_id)
        # Verify 6 plume horizons
        self.assertEqual(len(plume["horizons"]), 6)
        expected_plume_horizons = [0, 30, 60, 120, 180, 360]
        for idx, h in enumerate(plume["horizons"]):
            self.assertEqual(h["minutes"], expected_plume_horizons[idx])

    def test_unknown_hotspot_returns_none(self):
        result = self.service.get_plume("non-existent-hotspot-999")
        self.assertIsNone(result)
        
        forecast_result = self.service.get_forecast("non-existent-hotspot-999")
        self.assertIsNone(forecast_result)
        
        exposure_result = self.service.get_exposure("non-existent-hotspot-999")
        self.assertIsNone(exposure_result)

    def test_exposure_uses_dynamic_plume_context(self):
        hotspots = self.detector.run_detection()
        hs_id = hotspots[0].hotspot_id
        exposure = self.service.get_exposure(hs_id)
        self.assertIsNotNone(exposure)
        self.assertEqual(exposure["metadata"]["data_source"], "live_observation")
        self.assertGreater(exposure["estimated_population"], 0)

    def test_corridor_hotspot_matching(self):
        hotspots = self.detector.run_detection()
        observations = self.obs_repo.get_all()
        corridors = CorridorEngine.calculate_corridor_risks(hotspots, observations)
        self.assertGreater(len(corridors), 0)
        # Verify contributing hotspot is logically derived
        self.assertIn("contributing_hotspot_id", corridors[0])

    def test_synthetic_fallback_when_missing(self):
        empty_repo = InMemoryObservationRepository()
        empty_detector = HotspotDetectorService(empty_repo, self.ev_repo)
        empty_service = PredictionService(empty_detector, empty_repo)
        
        # When no observations exist, test fallback behavior
        fallback_context = empty_service._get_meteorological_context(28.0, 77.0)
        self.assertEqual(fallback_context["data_source"], "synthetic_demo_fallback")

if __name__ == "__main__":
    unittest.main()
