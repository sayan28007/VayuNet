from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from app.config import settings

router = APIRouter(prefix="/api/v1", tags=["Health"])


class SystemHealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    environment: str
    timestamp: str
    services: dict


@router.get("/health", response_model=SystemHealthResponse)
async def get_system_health():
    is_gemini_configured = bool(
        settings.GEMINI_API_KEY
        and settings.GEMINI_API_KEY != "your-gemini-api-key-here"
    )

    return SystemHealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc).isoformat(),
        services={
            "backend": "healthy",
            "gemini": "configured" if is_gemini_configured else "not_configured",
            "vertex_ai": "not_implemented",
            "bigquery": "not_implemented",
            "firebase": "not_implemented",
            "federation": "not_implemented",
        },
    )
