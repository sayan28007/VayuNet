from typing import List, Optional
import uuid

from app.models.observation import Observation
from app.models.hotspot import Hotspot
from app.models.evidence import ImageEvidence, EvidenceType
from app.repositories.observation_repo import get_repository
from app.repositories.evidence_repo import get_evidence_repository
from app.intelligence.anomaly import AnomalyDetector
from app.intelligence.clustering import SpatialClusterer
from app.intelligence.fusion import FusionEngine


class HotspotDetector:
    def __init__(self, observation_repository=None, evidence_repository=None):
        self.observation_repository = observation_repository or get_repository()
        self.evidence_repository = evidence_repository or get_evidence_repository()
        self.anomaly = AnomalyDetector()
        self.clusterer = SpatialClusterer()
        self.fusion = FusionEngine()

    def detect(
        self,
        observations: Optional[List[Observation]] = None,
        images: Optional[List[ImageEvidence]] = None,
    ) -> List[Hotspot]:
        observations = observations if observations is not None else self.observation_repository.get_all()
        if images is None:
            images = [
                item
                for item in self.evidence_repository.get_all()
                if getattr(item, "evidence_type", None) == EvidenceType.IMAGE
            ]

        if not observations:
            return []

        anomaly_scores = self.anomaly.sensor_anomaly_scores(observations)
        scores = dict(zip([o.id for o in observations], anomaly_scores))
        hotspots = []

        for group in self.clusterer.cluster(observations):
            if not group:
                continue

            lat = sum(o.latitude for o in group) / len(group)
            lon = sum(o.longitude for o in group) / len(group)
            density = min(1.0, len(group) / 5.0)
            source_types = set(str(o.source_type) for o in group)
            local_images = [
                i for i in images
                if abs(i.latitude - lat) < 0.05 and abs(i.longitude - lon) < 0.05
            ]
            citizen = any(str(o.source_type).endswith("citizen_report") for o in group)
            anomaly = max((scores.get(o.id, 0.0) for o in group), default=0.0)
            quality = sum(1.0 if o.data_quality_flag else 0.0 for o in group) / len(group)

            result = self.fusion.combine(
                anomaly,
                density,
                min(1.0, len(source_types) / 3.0),
                citizen,
                bool(local_images),
                quality,
            )

            if result["score"] < 0.30:
                continue

            pollutants = ["AQI"] if any(o.aqi is not None for o in group) else []
            if any(o.pm25 is not None for o in group):
                pollutants.append("PM2.5")

            explanation = (
                f"Detected from {len(group)} observation(s), anomaly score {anomaly:.2f}, "
                f"source diversity {len(source_types)}, and {len(local_images)} image evidence item(s)."
            )

            hotspots.append(
                Hotspot(
                    hotspot_id=str(uuid.uuid4()),
                    latitude=lat,
                    longitude=lon,
                    score=result["score"],
                    hotspot_score=result["score"],
                    confidence=result["confidence"],
                    severity=result["severity"],
                    evidence_count=len(group) + len(local_images),
                    source_types=sorted(source_types),
                    pollutant_list=pollutants,
                    anomaly_score=anomaly,
                    spatial_score=density,
                    data_quality_score=quality,
                    explanation=explanation,
                    city=group[0].city,
                    corridor=getattr(group[0], "corridor", None),
                )
            )

        return sorted(hotspots, key=lambda h: h.score, reverse=True)


class HotspotDetectorService:
    def __init__(self, observation_repository=None, evidence_repository=None):
        self.detector = HotspotDetector(observation_repository, evidence_repository)

    def run_detection(self) -> List[Hotspot]:
        return self.detector.detect()

    def detect(self, observations: Optional[List[Observation]] = None, images: Optional[List[ImageEvidence]] = None) -> List[Hotspot]:
        return self.detector.detect(observations, images)
