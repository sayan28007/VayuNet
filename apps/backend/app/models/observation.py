from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class SourceType(str, Enum):
    CITIZEN_REPORT = "citizen_report"
    LOCAL_SENSOR = "local_sensor"
    OFFICIAL_MONITOR = "official_monitor"
    METEOROLOGICAL = "meteorological"
    SATELLITE = "satellite"
    SYNTHETIC_DEMO = "synthetic_demo"

class ObservationBase(BaseModel):
    timestamp: datetime
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")
    source_type: SourceType
    source_id: str
    city: Optional[str] = None
    corridor: Optional[str] = None
    
    # Pollutants
    aqi: Optional[float] = Field(None, ge=0, le=1000)
    pm25: Optional[float] = Field(None, ge=0)
    pm10: Optional[float] = Field(None, ge=0)
    no2: Optional[float] = Field(None, ge=0)
    so2: Optional[float] = Field(None, ge=0)
    co: Optional[float] = Field(None, ge=0)
    o3: Optional[float] = Field(None, ge=0)
    
    # Weather
    temperature: Optional[float] = None
    humidity: Optional[float] = Field(None, ge=0, le=100)
    wind_speed: Optional[float] = Field(None, ge=0)
    wind_direction: Optional[float] = Field(None, ge=0, le=360)
    rainfall: Optional[float] = Field(None, ge=0)
    
    # Metadata
    confidence: float = Field(..., ge=0.0, le=1.0)
    data_quality_flag: bool = True

class ObservationCreate(ObservationBase):
    pass

class Observation(ObservationBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

