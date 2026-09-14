from .health import router as health_router
from .observations import router as observations_router
from .geospatial import router as geospatial_router
from .evidence import router as evidence_router
from .hotspots import router as hotspots_router

__all__ = [
    "health_router",
    "observations_router",
    "geospatial_router",
    "evidence_router",
    "hotspots_router",
]
