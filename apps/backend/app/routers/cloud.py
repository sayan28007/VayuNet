from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.cloud.bigquery import BigQueryService
from app.cloud.earth_engine import EarthEngineService
from app.cloud.secret_manager import SecretManagerService
from app.cloud.vertex_ai import VertexAIService
from app.repositories.observation_repo import ObservationRepository, get_repository

router = APIRouter(prefix="/api/v1/cloud", tags=["Google Cloud"])


class CloudStatusResponse(BaseModel):
    bigquery: dict
    secret_manager: dict
    vertex_ai: dict
    earth_engine: dict


class SyncResponse(BaseModel):
    status: str
    inserted: int = 0
    errors: List[dict] = Field(default_factory=list)


def get_observation_repository() -> ObservationRepository:
    return get_repository()


@router.get("/status", response_model=CloudStatusResponse)
def cloud_status() -> CloudStatusResponse:
    return CloudStatusResponse(
        bigquery={
            "status": "configured" if BigQueryService().is_configured() else "not_configured",
            "project_id": BigQueryService().project_id or None,
            "dataset": BigQueryService().dataset_id,
            "table": BigQueryService().table_id,
        },
        secret_manager=SecretManagerService().get_status(),
        vertex_ai=VertexAIService().get_status(),
        earth_engine=EarthEngineService().get_status(),
    )


@router.post("/bigquery/sync", response_model=SyncResponse)
def sync_observations(
    repository: ObservationRepository = Depends(get_observation_repository),
) -> SyncResponse:
    try:
        result = BigQueryService().sync_observations(repository.get_all())
        if result.get("status") not in {"ready", "partial_failure"}:
            raise HTTPException(status_code=503, detail=result)
        return SyncResponse(
            status=result.get("status", "unknown"),
            inserted=result.get("inserted", 0),
            errors=result.get("errors", []),
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"BigQuery sync failed: {exc}") from exc


@router.get("/bigquery/observations")
def query_observations(limit: int = Query(50, ge=1, le=500)):
    try:
        return BigQueryService().query_recent(limit)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"BigQuery query failed: {exc}") from exc


@router.get("/earth-engine/latest")
def earth_engine_latest(days: int = Query(7, ge=1, le=30)):
    try:
        return EarthEngineService().get_latest_image_metadata(days)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Earth Engine request failed: {exc}") from exc


@router.get("/secret-manager/status")
def secret_manager_status():
    return SecretManagerService().get_status()


@router.post("/vertex-ai/generate")
def vertex_ai_generate(payload: dict):
    prompt = str(payload.get("prompt", "")).strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt is required")
    try:
        return {
            "model": VertexAIService().model_name,
            "text": VertexAIService().generate_text(prompt),
        }
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Vertex AI request failed: {exc}") from exc
