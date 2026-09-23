from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from app.config import settings


class EarthEngineService:
    def __init__(self) -> None:
        self.project_id = self._resolve_project_id()
        self.collection_id = settings.EARTH_ENGINE_COLLECTION
        self._initialized = False

    @staticmethod
    def _resolve_project_id() -> str:
        project = settings.GOOGLE_CLOUD_PROJECT.strip()
        if project and project != "your-gcp-project-id":
            return project
        fallback = settings.GCP_PROJECT_ID.strip()
        if fallback and fallback != "your-gcp-project-id":
            return fallback
        return ""

    def is_configured(self) -> bool:
        return bool(self.project_id and self.collection_id.strip())

    def _initialize(self) -> None:
        if not self.is_configured():
            raise RuntimeError("Earth Engine is not configured")
        if self._initialized:
            return

        import google.auth
        import ee

        credentials, _ = google.auth.default()
        ee.Initialize(credentials=credentials, project=self.project_id)
        self._initialized = True

    def get_latest_image_metadata(self, days: int = 7) -> Dict[str, Any]:
        self._initialize()

        import ee

        days = max(1, min(int(days), 30))
        end = datetime.now(timezone.utc)
        start = end - timedelta(days=days)

        collection = (
            ee.ImageCollection(self.collection_id)
            .filterDate(start.isoformat(), end.isoformat())
            .sort("system:time_start", False)
        )
        image = collection.first()
        image_info = image.getInfo()
        if not image_info:
            return {
                "collection": self.collection_id,
                "found": False,
                "window_days": days,
            }

        properties = image_info.get("properties", {})
        return {
            "collection": self.collection_id,
            "found": True,
            "image_id": image_info.get("id"),
            "timestamp": properties.get("system:time_start"),
            "product_id": properties.get("PRODUCT_ID"),
            "platform": properties.get("PLATFORM"),
            "sensor": properties.get("SENSOR"),
            "quality": properties.get("PRODUCT_QUALITY"),
            "window_days": days,
        }

    def get_status(self) -> dict:
        return {
            "status": "configured" if self.is_configured() else "not_configured",
            "project_id": self.project_id or None,
            "collection": self.collection_id,
        }
