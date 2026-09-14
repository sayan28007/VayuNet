import unittest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from main import app
from app.repositories.observation_repo import get_repository

class TestObservationsAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        get_repository().delete_all()
        self.valid_time = datetime.now(timezone.utc).isoformat()
        
    def test_create_valid_observation(self):
        payload = {
            "timestamp": self.valid_time,
            "latitude": 17.68,
            "longitude": 83.21,
            "source_type": "synthetic_demo",
            "source_id": "test-1",
            "city": "TestCity",
            "aqi": 100,
            "confidence": 1.0
        }
        res = self.client.post("/api/v1/observations", json=payload)
        self.assertEqual(res.status_code, 200)
        
    def test_duplicate_observation_rejected(self):
        payload = {
            "timestamp": self.valid_time,
            "latitude": 17.68,
            "longitude": 83.21,
            "source_type": "synthetic_demo",
            "source_id": "duplicate-test",
            "confidence": 1.0
        }
        res1 = self.client.post("/api/v1/observations", json=payload)
        self.assertEqual(res1.status_code, 200)
        
        # Second identical payload must return 409 Conflict
        res2 = self.client.post("/api/v1/observations", json=payload)
        self.assertEqual(res2.status_code, 409)

    def test_invalid_latitude_longitude(self):
        payload_lat = {
            "timestamp": self.valid_time,
            "latitude": 95.0, # Invalid > 90
            "longitude": 83.21,
            "source_type": "synthetic_demo",
            "source_id": "test-lat",
            "confidence": 1.0
        }
        self.assertEqual(self.client.post("/api/v1/observations", json=payload_lat).status_code, 422)
        
        payload_lon = {
            "timestamp": self.valid_time,
            "latitude": 17.68,
            "longitude": -185.0, # Invalid < -180
            "source_type": "synthetic_demo",
            "source_id": "test-lon",
            "confidence": 1.0
        }
        self.assertEqual(self.client.post("/api/v1/observations", json=payload_lon).status_code, 422)

    def test_invalid_future_timestamp(self):
        future = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        payload = {
            "timestamp": future,
            "latitude": 17.68,
            "longitude": 83.21,
            "source_type": "synthetic_demo",
            "source_id": "test-future",
            "confidence": 1.0
        }
        res = self.client.post("/api/v1/observations", json=payload)
        self.assertEqual(res.status_code, 400)
        
    def _seed_geospatial_data(self):
        base = datetime.now(timezone.utc)
        self.client.post("/api/v1/observations", json={
            "timestamp": (base - timedelta(minutes=10)).isoformat(),
            "latitude": 10.0, "longitude": 10.0, "source_type": "synthetic_demo",
            "source_id": "1", "city": "CityA", "corridor": "Corr1", "aqi": 100, "confidence": 1.0
        })
        self.client.post("/api/v1/observations", json={
            "timestamp": (base - timedelta(minutes=5)).isoformat(),
            "latitude": 20.0, "longitude": 20.0, "source_type": "synthetic_demo",
            "source_id": "2", "city": "CityB", "corridor": "Corr1", "aqi": 200, "confidence": 1.0
        })
        self.client.post("/api/v1/observations", json={
            "timestamp": base.isoformat(),
            "latitude": 21.0, "longitude": 21.0, "source_type": "synthetic_demo",
            "source_id": "3", "city": "CityC", "corridor": "Corr2", "aqi": 50, "confidence": 1.0
        })

    def test_city_and_corridor_filtering(self):
        self._seed_geospatial_data()
        
        res_city = self.client.get("/api/v1/observations?city=CityA")
        self.assertEqual(len(res_city.json()), 1)
        self.assertEqual(res_city.json()[0]["city"], "CityA")

        res_corr = self.client.get("/api/v1/observations?corridor=Corr1")
        self.assertEqual(len(res_corr.json()), 2)
        
    def test_bbox_filtering(self):
        self._seed_geospatial_data()
        res = self.client.get("/api/v1/observations?min_lat=15&max_lat=25&min_lon=15&max_lon=25")
        data = res.json()
        self.assertEqual(len(data), 2)
        cities = [d["city"] for d in data]
        self.assertIn("CityB", cities)
        self.assertIn("CityC", cities)

    def test_radius_filtering(self):
        self._seed_geospatial_data()
        # Approx 140km between 20.0/20.0 and 21.0/21.0 (CityB & CityC). CityA is very far.
        # Check within 200km of CityB (20.0, 20.0) -> Should return CityB and CityC
        res = self.client.get("/api/v1/observations?center_lat=20.0&center_lon=20.0&radius_km=200")
        data = res.json()
        self.assertEqual(len(data), 2)
        cities = [d["city"] for d in data]
        self.assertIn("CityB", cities)
        self.assertIn("CityC", cities)

    def test_hotspot_heuristic(self):
        self._seed_geospatial_data()
        # Only CityB has AQI > 150 (it's 200)
        res = self.client.get("/api/v1/hotspots")
        data = res.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["city"], "CityB")
        
    def test_city_and_corridor_listings(self):
        self._seed_geospatial_data()
        res_cities = self.client.get("/api/v1/cities")
        self.assertEqual(res_cities.json(), ["CityA", "CityB", "CityC"])
        
        res_corr = self.client.get("/api/v1/corridors")
        self.assertEqual(res_corr.json(), ["Corr1", "Corr2"])

if __name__ == "__main__":
    unittest.main()

