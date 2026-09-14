import math
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

class PlumeEngine:
    """
    Prototype atmospheric plume dispersion model using wind vectors.
    Note: Not a certified dispersion model; designed for hackathon simulation.
    """
    @staticmethod
    def calculate_plume(
        hotspot_id: str,
        lat: float,
        lon: float,
        intensity: float,
        wind_speed_kmh: float,
        wind_direction_deg: float,
        horizons_minutes: List[int] = [0, 30, 60, 120, 180]
    ) -> Dict[str, Any]:
        horizons_output = []
        base_time = datetime.now(timezone.utc)
        
        # Convert wind direction (meteorological: direction FROM which wind blows) 
        # to transport direction (direction TO which plume travels)
        transport_dir_rad = math.radians((wind_direction_deg + 180) % 360)
        
        for mins in horizons_minutes:
            time_offset_hours = mins / 60.0
            # Distance traveled = speed * time
            distance_km = wind_speed_kmh * time_offset_hours
            
            # Approximate lat/lon offset (1 degree lat ~= 111 km, lon varies by cos(lat))
            lat_offset = (distance_km * math.cos(transport_dir_rad)) / 111.0
            lon_offset = (distance_km * math.sin(transport_dir_rad)) / (111.0 * math.cos(math.radians(lat)))
            
            center_lat = lat + lat_offset
            center_lon = lon + lon_offset
            
            # Radius expands with time and intensity (diffusion approximation)
            radius_km = max(1.0, 2.0 + (time_offset_hours * 1.5) + (intensity * 2.0))
            current_intensity = max(0.1, intensity * (1.0 / (1.0 + 0.2 * time_offset_hours)))
            
            # Simple bounding polygon generation (4 points around center)
            polygon = [
                {"lat": center_lat + (radius_km / 111.0), "lon": center_lon},
                {"lat": center_lat, "lon": center_lon + (radius_km / (111.0 * math.cos(math.radians(center_lat))))},
                {"lat": center_lat - (radius_km / 111.0), "lon": center_lon},
                {"lat": center_lat, "lon": center_lon - (radius_km / (111.0 * math.cos(math.radians(center_lat))))}
            ]
            
            horizons_output.append({
                "minutes": mins,
                "center_latitude": round(center_lat, 5),
                "center_longitude": round(center_lon, 5),
                "radius_km": round(radius_km, 2),
                "intensity": round(current_intensity, 2),
                "polygon": polygon
            })

        return {
            "hotspot_id": hotspot_id,
            "generated_at": base_time.isoformat(),
            "model": "prototype_plume_v1",
            "horizons": horizons_output
        }
