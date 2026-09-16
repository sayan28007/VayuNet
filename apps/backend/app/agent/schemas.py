from typing import List, Dict, Any
from pydantic import BaseModel, Field

class AgentChatRequest(BaseModel):
    message: str
    language: str = Field("en", description="Language code: en, hi, te")

class AgentChatResponse(BaseModel):
    answer: str
    tools_used: List[str] = []
    grounding: List[Dict[str, Any]] = []
    data_sources: List[str] = []
    tool_selection_mode: str = "backend_query_router"
    language: str = "en"
