import os
from typing import Dict, Any, List
from app.agent.tools import VayuNetTools
from app.agent.prompts import SYSTEM_PROMPT

class GeminiAgentService:
    def __init__(self, tools: VayuNetTools):
        self.tools = tools
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-pro")

    def process_query(self, message: str, language: str = "en") -> Dict[str, Any]:
        if not self.api_key:
            return {
                "answer": "gemini_not_configured: GEMINI_API_KEY environment variable is not set.",
                "tools_used": [],
                "grounding": [],
                "data_sources": ["gemini_not_configured"],
                "tool_selection_mode": "backend_query_router",
                "language": language
            }

        msg_lower = message.lower()
        tools_used = []
        grounding_data = []

        if "hotspot" in msg_lower or "severe" in msg_lower or "risk" in msg_lower or "severity" in msg_lower or "delhi" in msg_lower:
            hotspots = self.tools.get_active_hotspots()
            tools_used.append("get_active_hotspots")
            grounding_data.append({"hotspots": hotspots})
        
        if "forecast" in msg_lower or "predict" in msg_lower or "move" in msg_lower or "plume" in msg_lower or "aqi" in msg_lower:
            hotspots = self.tools.get_active_hotspots()
            hs_id = hotspots[0]["hotspot_id"] if hotspots else "hs-1"
            forecast = self.tools.get_forecast(hs_id)
            plume = self.tools.get_plume(hs_id)
            tools_used.extend(["get_forecast", "get_plume"])
            grounding_data.append({"forecast": forecast, "plume": plume})

        if "corridor" in msg_lower:
            corridors = self.tools.get_corridor_forecasts()
            tools_used.append("get_corridor_forecasts")
            grounding_data.append({"corridors": corridors})

        if "people" in msg_lower or "population" in msg_lower or "affected" in msg_lower or "expose" in msg_lower:
            hotspots = self.tools.get_active_hotspots()
            hs_id = hotspots[0]["hotspot_id"] if hotspots else "hs-1"
            exposure = self.tools.get_population_exposure(hs_id)
            tools_used.append("get_population_exposure")
            grounding_data.append({"exposure": exposure})

        if "authority" in msg_lower or "respond" in msg_lower or "alert" in msg_lower or "acknowledge" in msg_lower or "handle" in msg_lower or "source" in msg_lower:
            alerts = self.tools.get_active_alerts()
            authorities = self.tools.get_authority_status()
            tools_used.extend(["get_active_alerts", "get_authority_status"])
            grounding_data.append({"alerts": alerts, "authorities": authorities})

        if not tools_used:
            hotspots = self.tools.get_active_hotspots()
            tools_used.append("get_active_hotspots")
            grounding_data.append({"hotspots": hotspots})

        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=SYSTEM_PROMPT
            )
            prompt_payload = (
                f"User Query ({language}): {message}\n"
                f"Backend Tool Results: {grounding_data}\n"
                f"Instructions: Answer the user query strictly based on the backend tool results above. "
                f"Maintain numerical precision and use 'Likely source' attribution."
            )
            response = model.generate_content(prompt_payload)
            answer = response.text
            data_sources = ["gemini_api", "backend_repository"]
        except Exception as e:
            answer = f"Gemini API invocation error: {str(e)}. Grounding data was retrieved successfully via tools: {tools_used}."
            data_sources = ["gemini_api_error", "backend_repository"]

        return {
            "answer": answer,
            "tools_used": tools_used,
            "grounding": grounding_data,
            "data_sources": data_sources,
            "tool_selection_mode": "backend_query_router",
            "language": language
        }
