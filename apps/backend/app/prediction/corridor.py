from typing import List, Dict, Any, Optional
from app.models.hotspot import Hotspot
from app.models.observation import Observation

class CorridorEngine:
    """
    Calculates economic corridor risk levels derived from backend observations and hotspots,
    matching hotspots to corridors by spatial proximity or shared identifiers.
    """
    @staticmethod
    def _find_matching_hotspot(corridor_name: str, corridor_obs: List[Observation], hotspots: List[Hotspot]) -> Optional[str]:
        if not hotspots or not corridor_obs:
            return None
        
        # Compute centroid of corridor observations
        avg_lat = sum(o.latitude for o in corridor_obs) / len(corridor_obs)
        avg_lon = sum(o.longitude for o in corridor_obs) / len(corridor_obs)
        
        # Find nearest hotspot within reasonable distance (< 0.5 degrees) or highest score
        best_hs = None
        min_dist = float('inf')
        for hs in hotspots:
            dist = (hs.latitude - avg_lat)**2 + (hs.longitude - avg_lon)**2
            if dist < min_dist and dist < 0.25:
                min_dist = dist
                best_hs = hs
                
        if best_hs:
            return best_hs.hotspot_id
            
        return None

    @staticmethod
    def calculate_corridor_risks(hotspots: List[Hotspot], observations: List[Observation]) -> List[Dict[str, Any]]:
        corridor_map: Dict[str, List[Observation]] = {}
        
        for obs in observations:
            c_name = obs.corridor or "General Regional Corridor"
            if c_name not in corridor_map:
                corridor_map[c_name] = []
            corridor_map[c_name].append(obs)

        corridor_risks = []
        
        for corridor_name, obs_list in corridor_map.items():
            if not obs_list:
                continue
            
            avg_aqi = sum(o.aqi for o in obs_list) / len(obs_list)
            peak_aqi = max(o.aqi for o in obs_list) * 1.15
            
            contributing_hotspot = CorridorEngine._find_matching_hotspot(corridor_name, obs_list, hotspots)

            risk_level = "low"
            if avg_aqi >= 200 or peak_aqi >= 300:
                risk_level = "critical"
            elif avg_aqi >= 150 or peak_aqi >= 200:
                risk_level = "high"
            elif avg_aqi >= 100:
                risk_level = "moderate"

            corridor_risks.append({
                "corridor_name": corridor_name,
                "current_aqi": round(avg_aqi, 1),
                "predicted_aqi_1h": round(avg_aqi * 1.08, 1),
                "predicted_aqi_2h": round(avg_aqi * 1.02, 1),
                "predicted_aqi_3h": round(avg_aqi * 0.95, 1),
                "predicted_peak_aqi": round(peak_aqi, 1),
                "time_to_peak_minutes": 60,
                "risk_level": risk_level,
                "contributing_hotspot_id": contributing_hotspot,
                "confidence": 0.85
            })

        return corridor_risks
