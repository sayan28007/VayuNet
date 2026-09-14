from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel, Field
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
    gemini_status = "configured" if is_gemini_configured else "not_configured"

    return SystemHealthResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc).isoformat(),
        services={
            "backend": "healthy",
            "gemini": gemini_status,
            "vertex_ai": "not_implemented",
            "bigquery": "not_implemented",
            "firebase": "not_implemented",
            "federation": "not_implemented",
        },
    )
