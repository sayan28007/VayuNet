from datetime import datetime, timezone, timedelta
import random
from app.models.observation import ObservationCreate, SourceType
from app.services.observation_service import ObservationService

def seed_synthetic_data(service: ObservationService):
    random.seed(42)
    now=datetime.now(timezone.utc)
    locations=[
        {"city":"Visakhapatnam","lat":17.6868,"lon":83.2185,"corridor":"East Coast"},
        {"city":"Mumbai","lat":19.0760,"lon":72.8777,"corridor":"DMIC"},
        {"city":"Delhi","lat":28.7041,"lon":77.1025,"corridor":"DMIC"},
        {"city":"Bangalore","lat":12.9716,"lon":77.5946,"corridor":"South Tech"},
    ]
    for i in range(20):
        loc=random.choice(locations); aqi=random.uniform(50,300)
        service.create_observation(ObservationCreate(timestamp=now-timedelta(minutes=i+1),latitude=loc["lat"]+random.uniform(-0.01,0.01),longitude=loc["lon"]+random.uniform(-0.01,0.01),source_type=SourceType.SYNTHETIC_DEMO,source_id=f"demo-sensor-{i}",city=loc["city"],corridor=loc["corridor"],aqi=aqi,pm25=aqi*0.4,temperature=random.uniform(25,35),humidity=random.uniform(40,90),confidence=0.95))
