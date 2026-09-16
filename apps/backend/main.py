from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.repositories.observation_repo import get_repository
from app.repositories.evidence_repo import get_evidence_repository
from app.services.observation_service import ObservationService
from app.data.synthetic_seed import seed_synthetic_data

from app.routers import observations, geospatial, evidence, hotspots, predictions
from app.routers import agent, alerts

app = FastAPI(title="VayuNet Backend API", version="5.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    obs_service = ObservationService(get_repository())
    ev_repo = get_evidence_repository()
    seed_synthetic_data(obs_service, ev_repo)

@app.get("/")
def read_root():
    return {"status": "operational", "system": "VayuNet Phase 5 Intelligence & Response"}

app.include_router(observations.router)
app.include_router(geospatial.router)
app.include_router(evidence.router)
app.include_router(hotspots.router)
app.include_router(predictions.router)
app.include_router(agent.router)
app.include_router(alerts.router)
