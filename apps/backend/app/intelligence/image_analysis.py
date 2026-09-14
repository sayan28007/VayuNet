from pathlib import Path
from app.models.evidence import ImageEvidence, EvidenceType

def simulate_multimodal_vision(filename: str, latitude: float, longitude: float) -> ImageEvidence:
    name=Path(filename).name.lower()
    smoke=0.90 if "smoke" in name or "burn" in name else 0.20
    dust=0.15 if "dust" not in name else 0.75
    fire=0.10 if "fire" not in name else 0.85
    haze=0.25 if "haze" not in name else 0.70
    cats=[]
    if smoke>=0.6: cats.append("smoke")
    if dust>=0.6: cats.append("dust")
    if fire>=0.6: cats.append("fire")
    if haze>=0.6: cats.append("haze")
    return ImageEvidence(evidence_id=f"img-{filename}",latitude=latitude,longitude=longitude,confidence=max(smoke,dust,fire,haze),filename=filename,visible_smoke=smoke,dust=dust,fire=fire,haze=haze,detected_categories=cats,is_synthetic=True)
