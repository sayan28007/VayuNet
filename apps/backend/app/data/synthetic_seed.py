from datetime import datetime, timezone, timedelta
from app.models.observation import ObservationCreate, SourceType
from app.models.evidence import CitizenEvidenceCreate, CitizenReportCategory
from app.services.observation_service import ObservationService
from app.repositories.evidence_repo import EvidenceRepository
from app.routers.evidence import submit_citizen_evidence
import random

def seed_synthetic_data(obs_service: ObservationService, ev_repo: EvidenceRepository):
    random.seed(42)
    now = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    
    # 1. Normal Background Noise (Bangalore - Clean)
    for i in range(5):
        obs_service.create_observation(ObservationCreate(
            timestamp=now - timedelta(minutes=random.randint(1, 60)),
            latitude=12.9716 + random.uniform(-0.02, 0.02),
            longitude=77.5946 + random.uniform(-0.02, 0.02),
            source_type=SourceType.SYNTHETIC_DEMO,
            source_id=f"bg-sensor-{i}",
            city="Bangalore",
            aqi=random.uniform(30, 60),
            confidence=0.9
        ))

    # 2. Phase 4 Hotspot Candidate A: Delhi (Severe Anomaly + Meteorological context)
    for i in range(6):
        obs_service.create_observation(ObservationCreate(
            timestamp=now - timedelta(minutes=random.randint(1, 30)),
            latitude=28.7041 + random.uniform(-0.01, 0.01),
            longitude=77.1025 + random.uniform(-0.01, 0.01),
            source_type=SourceType.SYNTHETIC_DEMO,
            source_id=f"delhi-spike-{i}",
            city="Delhi",
            aqi=random.uniform(300, 450),
            pm25=random.uniform(200, 300),
            confidence=0.95
        ))
    
    ev_repo.save(submit_citizen_evidence(
        CitizenEvidenceCreate(
            latitude=28.7050,
            longitude=77.1030,
            category=CitizenReportCategory.SMOKE,
            text="Thick industrial smoke plume visible across NH-44 corridor",
            timestamp=now
        ), ev_repo
    ))
