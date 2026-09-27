from fastapi import APIRouter, HTTPException
from typing import List
from app.intelligence.hotspot_detector import HotspotDetector

router = APIRouter(prefix="/api/v1/hotspots", tags=["Hotspots"])


def get_detector() -> HotspotDetector:
    return HotspotDetector()


@router.get("", response_model=List[dict])
def get_hotspots():
    detector = get_detector()
    return [hotspot.model_dump() for hotspot in detector.detect()]


@router.post("/detect", response_model=List[dict])
def detect_hotspots():
    detector = get_detector()
    return [hotspot.model_dump() for hotspot in detector.detect()]


@router.get("/{hotspot_id}", response_model=dict)
def get_hotspot(hotspot_id: str):
    detector = get_detector()
    hotspots = detector.detect()
    for hotspot in hotspots:
        if hotspot.hotspot_id == hotspot_id:
            return hotspot.model_dump()
    raise HTTPException(status_code=404, detail="Hotspot not found")
