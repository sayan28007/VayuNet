from __future__ import annotations

from app.config import settings


class VertexAIService:
    def __init__(self) -> None:
        self.project_id = self._resolve_project_id()
        self.location = settings.GOOGLE_CLOUD_LOCATION
        self.model_name = settings.VERTEX_AI_MODEL_NAME

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
        return bool(self.project_id and self.model_name.strip())

    def generate_text(self, prompt: str) -> str:
        if not self.is_configured():
            raise RuntimeError("Vertex AI is not configured")
        if not prompt.strip():
            raise ValueError("Prompt must not be empty")

        from google import genai
        from google.genai.types import HttpOptions

        client = genai.Client(
            vertexai=True,
            project=self.project_id,
            location=self.location,
            http_options=HttpOptions(api_version="v1"),
        )
        response = client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Vertex AI returned an empty response")
        return text

    def get_status(self) -> dict:
        return {
            "status": "configured" if self.is_configured() else "not_configured",
            "project_id": self.project_id or None,
            "location": self.location,
            "model": self.model_name,
        }
