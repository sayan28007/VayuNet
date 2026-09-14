from datetime import datetime, timezone, timedelta
from app.models.observation import ObservationCreate, SourceType
from app.services.observation_service import ObservationService
import random

def seed_synthetic_data(service: ObservationService):
    # Set seed for deterministic generation
    random.seed(42)
    
    # Establish a fixed reference time for stable testing
    now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    
    locations = [
        {"city": "Visakhapatnam", "lat": 17.6868, "lon": 83.2185, "corridor": "East Coast"},
        {"city": "Mumbai", "lat": 19.0760, "lon": 72.8777, "corridor": "DMIC"},
        {"city": "Delhi", "lat": 28.7041, "lon": 77.1025, "corridor": "DMIC"},
        {"city": "Bangalore", "lat": 12.9716, "lon": 77.5946, "corridor": "South Tech"}
    ]
    
    for i in range(20):
        loc = random.choice(locations)
        # Add slight geo jitter
        lat_jitter = loc["lat"] + random.uniform(-0.05, 0.05)
        lon_jitter = loc["lon"] + random.uniform(-0.05, 0.05)
        
        aqi_val = random.uniform(50, 300)
        
        obs = ObservationCreate(
            timestamp=now - timedelta(minutes=random.randint(1, 1440)),
            latitude=lat_jitter,
            longitude=lon_jitter,
            source_type=SourceType.SYNTHETIC_DEMO,
            source_id=f"demo-sensor-{i}",
            city=loc["city"],
            corridor=loc["corridor"],
            aqi=aqi_val,
            pm25=aqi_val * 0.4,
            temperature=random.uniform(25.0, 35.0),
            humidity=random.uniform(40.0, 90.0),
            confidence=0.95
        )
        # Suppress 409 duplicates if seed restarts add exact duplicates
        try:
            service.create_observation(obs)
        except Exception:
            pass

