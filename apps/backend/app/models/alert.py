from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class AlertStatus(str, Enum):
    DETECTED = "DETECTED"
    VALIDATING = "VALIDATING"
    HIGH_CONFIDENCE = "HIGH_CONFIDENCE"
    ROUTED = "ROUTED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    ACTION_IN_PROGRESS = "ACTION_IN_PROGRESS"
    RESOLVED = "RESOLVED"

VALID_TRANSITIONS: Dict[AlertStatus, List[AlertStatus]] = {
    AlertStatus.DETECTED: [AlertStatus.VALIDATING, AlertStatus.HIGH_CONFIDENCE],
    AlertStatus.VALIDATING: [AlertStatus.HIGH_CONFIDENCE, AlertStatus.DETECTED],
    AlertStatus.HIGH_CONFIDENCE: [AlertStatus.ROUTED],
    AlertStatus.ROUTED: [AlertStatus.ACKNOWLEDGED],
    AlertStatus.ACKNOWLEDGED: [AlertStatus.ACTION_IN_PROGRESS],
    AlertStatus.ACTION_IN_PROGRESS: [AlertStatus.RESOLVED],
    AlertStatus.RESOLVED: []
}

class AlertModel(BaseModel):
    event_id: str
    hotspot_id: str
    severity: str
    priority_score: float
    priority_level: str
    location: Dict[str, float]
    likely_source: str
    confidence: float
    affected_population: int
    corridor: str
    predicted_peak: float
    assigned_authority: str
    status: AlertStatus = AlertStatus.HIGH_CONFIDENCE
    routing_reason: str
    recommended_response: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
