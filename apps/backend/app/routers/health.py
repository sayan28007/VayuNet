from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.cloud.bigquery import BigQueryService
from app.cloud.earth_engine import EarthEngineService
from app.cloud.secret_manager import SecretManagerService
from app.cloud.vertex_ai import VertexAIService
from app.config import settings

router = APIRouter(prefix="/api/v1", tags=["Health & System Status"])


class SystemHealthResponse(BaseModel):
    status: str = Field(..., example="healthy")
    app_name: str = Field(..., example="VayuNet Intelligence Backend")
    version: str = Field(..., example="1.0.0")
    environment: str = Field(..., example="development")
    timestamp: str = Field(..., example="2026-09-10T21:43:49Z")
    services: dict


@router.get("/health", response_model=SystemHealthResponse)
async def get_system_health():
    is_gemini_configured = bool(
        settings.GEMINI_API_KEY
        and settings.GEMINI_API_KEY != "your-gemini-api-key-here"
    )

    cloud_services = {
        "bigquery": "configured" if BigQueryService().is_configured() else "not_configured",
        "secret_manager": SecretManagerService().get_status()["status"],
        "vertex_ai": VertexAIService().get_status()["status"],
        "earth_engine": EarthEngineService().get_status()["status"],
    }

    return SystemHealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc).isoformat(),
        services={
            "backend": "healthy",
            "gemini": "configured" if is_gemini_configured else "not_configured",
            "google_cloud": cloud_services,
            "federation": "available",
        },
    )
