import unittest
import os
from app.agent.tools import VayuNetTools
from app.agent.gemini_agent import GeminiAgentService
from app.intelligence.hotspot_detector import HotspotDetectorService
from app.prediction.prediction_service import PredictionService
from app.services.alert_service import AlertService
from app.repositories.observation_repo import InMemoryObservationRepository
from app.repositories.evidence_repo import get_evidence_repository

class TestPhase5Agent(unittest.TestCase):
    def setUp(self):
        AlertService.reset_store()
        self.obs_repo = InMemoryObservationRepository()
        self.ev_repo = get_evidence_repository()
        self.detector = HotspotDetectorService(self.obs_repo, self.ev_repo)
        self.prediction = PredictionService(self.detector, self.obs_repo)
        self.alert_service = AlertService(self.detector, self.prediction)
        self.tools = VayuNetTools(self.detector, self.prediction, self.alert_service, self.obs_repo)

    def test_gemini_not_configured_fallback(self):
        old_key = os.environ.get("GEMINI_API_KEY")
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]
        
        agent = GeminiAgentService(self.tools)
        res = agent.process_query("What are the active hotspots?", language="en")
        
        self.assertIn("gemini_not_configured", res["data_sources"])
        self.assertIn("gemini_not_configured", res["answer"])
        
        if old_key is not None:
            os.environ["GEMINI_API_KEY"] = old_key

    def test_tool_execution_and_grounding(self):
        hotspots = self.tools.get_active_hotspots()
        self.assertIsInstance(hotspots, list)

        corridors = self.tools.get_corridor_forecasts()
        self.assertIsInstance(corridors, list)

        federated = self.tools.get_federated_status()
        self.assertEqual(federated["status"], "not_implemented")

        model_ver = self.tools.get_model_version()
        self.assertEqual(model_ver["version"], "5.0.0")

    def test_unknown_hotspot_handling(self):
        unknown_id = "non-existent-hotspot"
        
        details = self.tools.get_hotspot_details(unknown_id)
        self.assertIsNone(details)

        forecast = self.tools.get_forecast(unknown_id)
        self.assertIsNone(forecast)

        plume = self.tools.get_plume(unknown_id)
        self.assertIsNone(plume)

        exposure = self.tools.get_population_exposure(unknown_id)
        self.assertIsNone(exposure)

if __name__ == "__main__":
    unittest.main()
