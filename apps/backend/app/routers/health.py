from datetime import datetime, timezone
from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.config import settings
from app.repositories.observation_repo import get_repository
from app.federation.coordinator import FederatedCoordinator

router = APIRouter(prefix="/api/v1", tags=["Health & System Status"])

class SystemHealthResponse(BaseModel):
    status: str = Field(..., example="healthy")
    app_name: str
    version: str
    environment: str
    timestamp: str
    services: dict

class ReadinessResponse(BaseModel):
    ready: bool
    checks: dict
    timestamp: str

@router.get("/health", response_model=SystemHealthResponse)
async def get_system_health():
    is_gemini_configured = bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your-gemini-api-key-here")
    try:
        observation_count = len(get_repository().get_all())
        backend_status = "healthy"
    except Exception:
        observation_count = 0
        backend_status = "degraded"
    federation_status = FederatedCoordinator.get_coordinator().get_federation_status()
    return SystemHealthResponse(
        status=backend_status,
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.now(timezone.utc).isoformat(),
        services={
            "backend": backend_status,
            "observations": "ready" if observation_count >= 0 else "degraded",
            "gemini": "configured" if is_gemini_configured else "not_configured",
            "vertex_ai": "not_implemented",
            "bigquery": "not_implemented",
            "firebase": "not_implemented",
            "federation": federation_status["status"].lower(),
        },
    )

@router.get("/ready", response_model=ReadinessResponse)
def get_readiness():
    checks = {}
    try:
        get_repository().get_all()
        checks["repository"] = "ready"
    except Exception as exc:
        checks["repository"] = f"error: {exc}"
    checks["federation"] = "ready"
    checks["configuration"] = "ready"
    ready = all(value == "ready" for value in checks.values())
    return ReadinessResponse(ready=ready, checks=checks, timestamp=datetime.now(timezone.utc).isoformat())
