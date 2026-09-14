from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from typing import Optional
from datetime import datetime, timezone
from app.models.evidence import Evidence, CitizenReportCreate
from app.repositories.evidence_repo import get_evidence_repository
from app.intelligence.image_analysis import analyze_image

router = APIRouter(prefix="/api/v1/evidence", tags=["Evidence"])

def get_repository():
    return get_evidence_repository()

@router.post("/citizen", response_model=Evidence)
def create_citizen_report(
    report: CitizenReportCreate,
    repo=Depends(get_repository),
):
    evidence = Evidence(
        timestamp=report.timestamp,
        latitude=report.latitude,
        longitude=report.longitude,
        source_type="citizen_report",
        source_id=report.source_id,
        city=report.city,
        corridor=report.corridor,
        report_text=report.report_text,
        confidence=report.confidence,
    )
    return repo.save(evidence)

@router.post("/photo", response_model=Evidence)
async def create_photo_evidence(
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    source_id: str = Form(...),
    timestamp: Optional[datetime] = Form(None),
    city: Optional[str] = Form(None),
    corridor: Optional[str] = Form(None),
    repo=Depends(get_repository),
):
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image upload")

    analysis_result = analyze_image(file.filename or "uploaded-image", image_bytes)

    evidence = Evidence(
        timestamp=timestamp or datetime.now(timezone.utc),
        latitude=latitude,
        longitude=longitude,
        source_type="citizen_report",
        source_id=source_id,
        city=city,
        corridor=corridor,
        media_filename=file.filename,
        image_analysis=analysis_result,
        confidence=analysis_result.confidence,
        is_synthetic=analysis_result.is_synthetic,
    )
    return repo.save(evidence)

@router.get("", response_model=list[Evidence])
def list_evidence(repo=Depends(get_repository)):
    return repo.get_all()
