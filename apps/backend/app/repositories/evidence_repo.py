from typing import Dict, List, Optional
from app.models.evidence import EvidenceBase

class EvidenceRepository:
    def __init__(self):
        self._data: Dict[str, EvidenceBase] = {}

    def save(self, evidence: EvidenceBase) -> EvidenceBase:
        self._data[evidence.evidence_id] = evidence
        return evidence

    def get_all(self) -> List[EvidenceBase]:
        return list(self._data.values())

    def get_by_id(self, evidence_id: str) -> Optional[EvidenceBase]:
        return self._data.get(evidence_id)

    def clear(self) -> None:
        self._data.clear()

_repo = EvidenceRepository()

def get_evidence_repository() -> EvidenceRepository:
    return _repo
