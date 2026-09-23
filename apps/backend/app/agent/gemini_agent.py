import os
from typing import Any, Dict

from app.agent.prompts import SYSTEM_PROMPT
from app.agent.tools import VayuNetTools
from app.cloud.secret_manager import SecretManagerService
from app.cloud.vertex_ai import VertexAIService
from app.config import settings


class GeminiAgentService:
    def __init__(self, tools: VayuNetTools):
        self.tools = tools
        self.api_key = os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL_NAME

    def _grounding(self, message: str) -> tuple[list[str], list[dict[str, Any]]]:
        msg_lower = message.lower()
        tools_used: list[str] = []
        grounding_data: list[dict[str, Any]] = []

        if any(term in msg_lower for term in ["hotspot", "severe", "risk", "severity", "delhi"]):
            grounding_data.append({"hotspots": self.tools.get_active_hotspots()})
            tools_used.append("get_active_hotspots")

        if any(term in msg_lower for term in ["forecast", "predict", "move", "plume", "aqi"]):
            hotspots = self.tools.get_active_hotspots()
            if hotspots:
                hotspot_id = hotspots[0]["hotspot_id"]
                grounding_data.append({
                    "forecast": self.tools.get_forecast(hotspot_id),
                    "plume": self.tools.get_plume(hotspot_id),
                })
                tools_used.extend(["get_forecast", "get_plume"])

        if "corridor" in msg_lower:
            grounding_data.append({"corridors": self.tools.get_corridor_forecasts()})
            tools_used.append("get_corridor_forecasts")

        if any(term in msg_lower for term in ["people", "population", "affected", "expose"]):
            hotspots = self.tools.get_active_hotspots()
            if hotspots:
                grounding_data.append({"exposure": self.tools.get_population_exposure(hotspots[0]["hotspot_id"])})
                tools_used.append("get_population_exposure")

        if any(term in msg_lower for term in ["authority", "respond", "alert", "acknowledge", "handle", "source"]):
            grounding_data.append({
                "alerts": self.tools.get_active_alerts(),
                "authorities": self.tools.get_authority_status(),
            })
            tools_used.extend(["get_active_alerts", "get_authority_status"])

        if not tools_used:
            grounding_data.append({"hotspots": self.tools.get_active_hotspots()})
            tools_used.append("get_active_hotspots")

        return tools_used, grounding_data

    def _build_prompt(self, message: str, language: str, grounding_data: list[dict[str, Any]]) -> str:
        return (
            f"{SYSTEM_PROMPT}\n\n"
            f"User Query ({language}): {message}\n"
            f"Backend Tool Results: {grounding_data}\n"
            "Answer strictly from the supplied backend data. Preserve numerical precision. "
            "Use 'Likely source' wording for source attribution and clearly state when data is unavailable."
        )

    def process_query(self, message: str, language: str = "en") -> Dict[str, Any]:
        tools_used, grounding_data = self._grounding(message)
        prompt = self._build_prompt(message, language, grounding_data)

        if settings.GEMINI_USE_VERTEX_AI and VertexAIService().is_configured():
            try:
                answer = VertexAIService().generate_text(prompt)
                return {
                    "answer": answer,
                    "tools_used": tools_used,
                    "grounding": grounding_data,
                    "data_sources": ["vertex_ai", "backend_repository"],
                    "tool_selection_mode": "backend_query_router",
                    "language": language,
                }
            except Exception as exc:
                vertex_error = str(exc)
        else:
            vertex_error = None

        api_key = self.api_key
        secret_error = None
        if not api_key and SecretManagerService().is_configured():
            try:
                api_key = SecretManagerService().access_secret()
            except Exception as exc:
                secret_error = str(exc)

        if not api_key:
            details = [item for item in [vertex_error, secret_error] if item]
            return {
                "answer": "gemini_not_configured: no usable Vertex AI or Gemini credential is available."
                + (f" Details: {' | '.join(details)}" if details else ""),
                "tools_used": tools_used,
                "grounding": grounding_data,
                "data_sources": ["backend_repository"],
                "tool_selection_mode": "backend_query_router",
                "language": language,
            }

        try:
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=SYSTEM_PROMPT,
            )
            response = model.generate_content(prompt)
            answer = response.text
            data_sources = ["gemini_api", "backend_repository"]
        except Exception as exc:
            answer = f"Gemini API invocation error: {exc}. Grounding data was retrieved successfully via tools: {tools_used}."
            data_sources = ["gemini_api_error", "backend_repository"]

        return {
            "answer": answer,
            "tools_used": tools_used,
            "grounding": grounding_data,
            "data_sources": data_sources,
            "tool_selection_mode": "backend_query_router",
            "language": language,
        }
