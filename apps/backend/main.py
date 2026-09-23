from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.agent import router as agent_router
from app.routers.alerts import router as alerts_router
from app.routers.cloud import router as cloud_router
from app.routers.demo import router as demo_router
from app.routers.evidence import router as evidence_router
from app.routers.federation import router as federation_router
from app.routers.geospatial import router as geospatial_router
from app.routers.health import router as health_router
from app.routers.hotspots import router as hotspots_router
from app.routers.observations import router as observations_router
from app.routers.predictions import router as predictions_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="VayuNet - AI-powered hyperlocal pollution intelligence and climate action platform.",
)

allowed_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(observations_router)
app.include_router(geospatial_router)
app.include_router(evidence_router)
app.include_router(hotspots_router)
app.include_router(predictions_router)
app.include_router(agent_router)
app.include_router(alerts_router)
app.include_router(federation_router)
app.include_router(demo_router)
app.include_router(cloud_router)

if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
