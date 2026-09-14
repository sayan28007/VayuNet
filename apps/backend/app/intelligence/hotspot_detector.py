from typing import List
import uuid
from app.models.observation import Observation
from app.models.hotspot import Hotspot
from app.models.evidence import ImageEvidence
from app.intelligence.anomaly import AnomalyDetector
from app.intelligence.clustering import SpatialClusterer
from app.intelligence.fusion import FusionEngine

class HotspotDetector:
    def __init__(self):
        self.anomaly=AnomalyDetector()
        self.clusterer=SpatialClusterer()
        self.fusion=FusionEngine()

    def detect(self, observations: List[Observation], images: List[ImageEvidence]|None=None) -> List[Hotspot]:
        images=images or []
        anomaly_scores=self.anomaly.sensor_anomaly_scores(observations)
        scores=dict(zip([o.id for o in observations],anomaly_scores))
        hotspots=[]
        for group in self.clusterer.cluster(observations):
            if not group: continue
            lat=sum(o.latitude for o in group)/len(group); lon=sum(o.longitude for o in group)/len(group)
            density=min(1.0,len(group)/5.0)
            src=set(str(o.source_type) for o in group)
            local_images=[i for i in images if abs(i.latitude-lat)<0.05 and abs(i.longitude-lon)<0.05]
            citizen=any(str(o.source_type).endswith("citizen_report") for o in group)
            anomaly=max((scores.get(o.id,0.0) for o in group),default=0.0)
            quality=sum(1.0 if o.data_quality_flag else 0.0 for o in group)/len(group)
            result=self.fusion.combine(anomaly,density,min(1.0,len(src)/3.0),citizen,bool(local_images),quality)
            if result["score"] < 0.30: continue
            pollutants=["AQI"] if any(o.aqi is not None for o in group) else []
            if any(o.pm25 is not None for o in group): pollutants.append("PM2.5")
            explanation=f"Detected from {len(group)} observation(s), anomaly score {anomaly:.2f}, source diversity {len(src)}, and {len(local_images)} image evidence item(s)."
            hotspots.append(Hotspot(hotspot_id=str(uuid.uuid4()),latitude=lat,longitude=lon,score=result["score"],confidence=result["confidence"],severity=result["severity"],evidence_count=len(group)+len(local_images),source_types=sorted(src),pollutant_list=pollutants,anomaly_score=anomaly,spatial_score=density,data_quality_score=quality,explanation=explanation,city=group[0].city))
        return sorted(hotspots,key=lambda h:h.score,reverse=True)
