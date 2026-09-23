from fastapi import APIRouter, Depends, HTTPException

from app.agent.gemini_agent import GeminiAgentService
from app.agent.schemas import AgentChatRequest, AgentChatResponse
from app.agent.tools import VayuNetTools
from app.repositories.evidence_repo import get_evidence_repository
from app.repositories.observation_repo import get_repository

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])


def get_agent_service() -> GeminiAgentService:
    tools = VayuNetTools(
        obs_repo=get_repository(),
        evidence_repo=get_evidence_repository(),
    )
    return GeminiAgentService(tools)


@router.post("/chat", response_model=AgentChatResponse)
def chat_with_agent(payload: AgentChatRequest, agent: GeminiAgentService = Depends(get_agent_service)):
    try:
        return AgentChatResponse(**agent.process_query(payload.message, payload.language))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
