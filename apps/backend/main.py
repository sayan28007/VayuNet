from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, observations, geospatial, evidence, hotspots, predictions
from app.repositories.observation_repo import get_repository
from app.repositories.evidence_repo import get_evidence_repository
from app.services.observation_service import ObservationService
from app.data.synthetic_seed import seed_synthetic_data

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

app.include_router(health.router)
app.include_router(observations.router)
app.include_router(geospatial.router)
app.include_router(evidence.router)
app.include_router(hotspots.router)
app.include_router(predictions.router)

@app.on_event("startup")
async def startup_event():
    obs_service = ObservationService(get_repository())
    ev_repo = get_evidence_repository()
    seed_synthetic_data(obs_service, ev_repo)
    print("Synthetic Phase 4 Prediction & Multimodal data seeded successfully.")

@app.get("/")
def read_root():
    return {"service": settings.APP_NAME, "status": "online"}
