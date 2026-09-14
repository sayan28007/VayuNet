from .health import router as health_router
from .observations import router as observations_router
from .geospatial import router as geospatial_router

__all__ = ["health_router", "observations_router", "geospatial_router"]

