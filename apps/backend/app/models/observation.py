from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class SourceType(str, Enum):
    CITIZEN_REPORT = "citizen_report"
    LOCAL_SENSOR = "local_sensor"
    OFFICIAL_MONITOR = "official_monitor"
    METEOROLOGICAL = "meteorological"
    SATELLITE = "satellite"
    SYNTHETIC_DEMO = "synthetic_demo"

class ObservationBase(BaseModel):
    timestamp: datetime
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    source_type: SourceType
    source_id: str
    city: str
    corridor: Optional[str] = None
    aqi: float = Field(..., ge=0.0, le=1000.0)
    pm25: Optional[float] = Field(None, ge=0.0)
    pm10: Optional[float] = Field(None, ge=0.0)
    no2: Optional[float] = Field(None, ge=0.0)
    so2: Optional[float] = Field(None, ge=0.0)
    co: Optional[float] = Field(None, ge=0.0)
    o3: Optional[float] = Field(None, ge=0.0)
    wind_speed_kmh: Optional[float] = Field(None, ge=0.0)
    wind_direction_deg: Optional[float] = Field(None, ge=0.0, le=360.0)
    weather_condition: Optional[str] = None
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    data_quality_flag: bool = True

class ObservationCreate(ObservationBase):
    pass

class Observation(ObservationBase):
    id: str
