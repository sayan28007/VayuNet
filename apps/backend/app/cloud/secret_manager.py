from __future__ import annotations

from app.config import settings


class SecretManagerService:
    def __init__(self) -> None:
        self.project_id = self._resolve_project_id()
        self.default_secret_id = settings.GEMINI_SECRET_ID

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
        return bool(self.project_id and self.default_secret_id.strip())

    def access_secret(self, secret_id: str | None = None, version: str = "latest") -> str:
        if not self.is_configured():
            raise RuntimeError("Secret Manager is not configured")

        from google.cloud import secretmanager

        secret_name = secret_id or self.default_secret_id
        name = f"projects/{self.project_id}/secrets/{secret_name}/versions/{version}"
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("utf-8")

    def get_status(self) -> dict:
        return {
            "status": "configured" if self.is_configured() else "not_configured",
            "secret_id": self.default_secret_id if self.is_configured() else None,
        }
