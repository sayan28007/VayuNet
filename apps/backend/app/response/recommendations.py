from typing import List

class RecommendationEngine:
    @staticmethod
    def get_recommendations(likely_source: str) -> List[str]:
        source_lower = likely_source.lower()
        if "industrial" in source_lower:
            return [
                "Conduct immediate on-site industrial stack inspection",
                "Verify continuous emission monitoring system (CEMS) telemetry",
                "Enforce temporary perimeter emission curtailment"
            ]
        elif "agricultural" in source_lower or "crop" in source_lower or "burning" in source_lower:
            return [
                "Dispatch district agricultural task force for field verification",
                "Coordinate with local enforcement for stubble burning suppression",
                "Issue advisory for surrounding agricultural zones"
            ]
        elif "waste" in source_lower:
            return [
                "Dispatch municipal inspection unit to municipal solid waste site",
                "Coordinate immediate fire suppression and waste clearing",
                "Verify illegal dumping prevention protocols"
            ]
        elif "traffic" in source_lower:
            return [
                "Deploy traffic congestion and heavy vehicle diversion units",
                "Increase remote sensing verification along transport arteries",
                "Issue urban traffic advisory"
            ]
        elif "exposure" in source_lower or "health" in source_lower:
            return [
                "Coordinate public health advisories with regional medical directorates",
                "Deploy mobile air quality monitoring units near sensitive receptors",
                "Issue vulnerable population health warning"
            ]
        else:
            return [
                "Conduct regional field reconnaissance and sensor calibration",
                "Verify stationary particulate sensor telemetry",
                "Monitor meteorological dispersion patterns"
            ]
