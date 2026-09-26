from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from typing import Optional
from pydantic import BaseModel, Field
from uuid import uuid4

from app.models.evidence import EvidenceBase, CitizenEvidence, ImageEvidence
from app.repositories.evidence_repo import get_evidence_repository
from app.intelligence.image_analysis import simulate_multimodal_vision

router = APIRouter(prefix="/api/v1/evidence", tags=["Evidence"])

def get_repository():
    return get_evidence_repository()

class CitizenReportCreate(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    source_id: str
    city: Optional[str] = None
    corridor: Optional[str] = None
    report_text: str
    confidence: float = Field(0.8, ge=0.0, le=1.0)

@router.post("/citizen", response_model=CitizenEvidence)
def create_citizen_report(
    report: CitizenReportCreate,
    repo=Depends(get_repository),
):
    evidence = CitizenEvidence(
        evidence_id=f"citizen-{uuid4().hex[:12]}",
        latitude=report.latitude,
        longitude=report.longitude,
        source_id=report.source_id,
        city=report.city,
        text=report.report_text,
        confidence=report.confidence,
    )
    evidence.metadata["corridor"] = report.corridor
    return repo.save(evidence)

@router.post("/photo", response_model=ImageEvidence)
async def create_photo_evidence(
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    source_id: str = Form(...),
    city: Optional[str] = Form(None),
    corridor: Optional[str] = Form(None),
    repo=Depends(get_repository),
):
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image upload")

    evidence = simulate_multimodal_vision(
        file.filename or "uploaded-image",
        latitude,
        longitude,
    )
    evidence.source_id = source_id
    evidence.city = city
    evidence.metadata["corridor"] = corridor
    return repo.save(evidence)

@router.get("", response_model=list[EvidenceBase])
def list_evidence(repo=Depends(get_repository)):
    return repo.get_all()
