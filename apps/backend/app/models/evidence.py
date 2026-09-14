from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class EvidenceType(str, Enum):
    SENSOR = "sensor"
    CITIZEN = "citizen"
    IMAGE = "image"

class EvidenceBase(BaseModel):
    evidence_id: str
    evidence_type: EvidenceType
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    source_id: Optional[str] = None
    city: Optional[str] = None
    metadata: dict = Field(default_factory=dict)

class ImageEvidence(EvidenceBase):
    evidence_type: EvidenceType = EvidenceType.IMAGE
    filename: Optional[str] = None
    visible_smoke: float = Field(0.0, ge=0.0, le=1.0)
    dust: float = Field(0.0, ge=0.0, le=1.0)
    fire: float = Field(0.0, ge=0.0, le=1.0)
    haze: float = Field(0.0, ge=0.0, le=1.0)
    detected_categories: List[str] = Field(default_factory=list)
    is_synthetic: bool = True

class CitizenEvidence(EvidenceBase):
    evidence_type: EvidenceType = EvidenceType.CITIZEN
    text: Optional[str] = None

class SensorEvidence(EvidenceBase):
    evidence_type: EvidenceType = EvidenceType.SENSOR
    aqi: Optional[float] = None
    pm25: Optional[float] = None
