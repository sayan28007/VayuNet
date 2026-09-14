from typing import Protocol, List, Optional
from datetime import datetime
from app.models.observation import Observation

class ObservationRepository(Protocol):
    def save(self, observation: Observation) -> Observation:
        ...
    def get_by_id(self, obs_id: str) -> Optional[Observation]:
        ...
    def get_all(self) -> List[Observation]:
        ...
    def delete_all(self) -> None:
        ...
    def exists(self, source_id: str, timestamp: datetime, lat: float, lon: float) -> bool:
        ...

class InMemoryObservationRepository:
    def __init__(self):
        self._data: dict[str, Observation] = {}

    def save(self, observation: Observation) -> Observation:
        self._data[observation.id] = observation
        return observation

    def get_by_id(self, obs_id: str) -> Optional[Observation]:
        return self._data.get(obs_id)

    def get_all(self) -> List[Observation]:
        return list(self._data.values())
        
    def delete_all(self) -> None:
        self._data.clear()
        
    def exists(self, source_id: str, timestamp: datetime, lat: float, lon: float) -> bool:
        for obs in self._data.values():
            if (obs.source_id == source_id and 
                obs.timestamp == timestamp and 
                obs.latitude == lat and 
                obs.longitude == lon):
                return True
        return False

# Global singleton for local development
_repo_instance = InMemoryObservationRepository()

def get_repository() -> ObservationRepository:
    return _repo_instance

