import unittest
from app.models.observation import Observation
from app.intelligence.hotspot_detector import HotspotDetector
from datetime import datetime, timezone

class TestIntelligence(unittest.TestCase):
    def test_detector_returns_list(self):
        obs=[Observation(timestamp=datetime.now(timezone.utc),latitude=28.7041,longitude=77.1025,source_type="synthetic_demo",source_id="a",aqi=120,confidence=1.0),Observation(timestamp=datetime.now(timezone.utc),latitude=28.705,longitude=77.103,source_type="synthetic_demo",source_id="b",aqi=320,confidence=1.0)]
        result=HotspotDetector().detect(obs,[])
        self.assertIsInstance(result,list)

if __name__=="__main__": unittest.main()
