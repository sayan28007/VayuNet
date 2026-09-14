from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class Hotspot(BaseModel):
    hotspot_id: str
    latitude: float
    longitude: float
    score: float = Field(..., ge=0.0, le=1.0)
    confidence: float = Field(..., ge=0.0, le=1.0)
    severity: str
    evidence_count: int = Field(..., ge=0)
    source_types: List[str] = Field(default_factory=list)
    pollutant_list: List[str] = Field(default_factory=list)
    anomaly_score: float = 0.0
    spatial_score: float = 0.0
    data_quality_score: float = 0.0
    explanation: str = ""
    city: Optional[str] = None
    metadata: Dict = Field(default_factory=dict)
