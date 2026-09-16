from typing import Tuple

class AuthorityService:
    @staticmethod
    def route_authority(
        likely_source: str,
        corridor: str,
        aqi: float
    ) -> Tuple[str, str, str]:
        source_lower = likely_source.lower()
        
        if "industrial" in source_lower:
            authority = "State Pollution Control Board (SPCB)"
            reason = f"Routed to {authority} due to industrial emission detection along {corridor} with peak AQI {aqi}."
            normalized_source = "Industrial Emission"
        elif "agricultural" in source_lower or "burning" in source_lower:
            authority = "Agriculture + District Administration"
            reason = f"Routed to {authority} due to agricultural burning signatures detected in {corridor}."
            normalized_source = "Agricultural Burning"
        elif "waste" in source_lower:
            authority = "Municipal authority"
            reason = f"Routed to {authority} due to solid waste burning and municipal site anomalies in {corridor}."
            normalized_source = "Waste Burning"
        elif "traffic" in source_lower:
            authority = "Traffic / Urban authority"
            reason = f"Routed to {authority} due to heavy traffic corridor emission congestion along {corridor}."
            normalized_source = "Traffic"
        elif aqi > 400.0:
            authority = "Health / Disaster authority"
            reason = f"Routed to {authority} due to severe public exposure threshold exceeded (AQI {aqi})."
            normalized_source = "Severe Public Exposure"
        else:
            authority = "State Pollution Control Board (SPCB)"
            reason = f"Routed to {authority} for standard environmental monitoring and verification in {corridor}."
            normalized_source = "General Urban Smog"

        return normalized_source, authority, reason
