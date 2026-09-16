from fastapi import APIRouter, Depends, HTTPException
from app.agent.schemas import AgentChatRequest, AgentChatResponse
from app.agent.gemini_agent import GeminiAgentService
from app.agent.tools import VayuNetTools
from app.intelligence.hotspot_detector import HotspotDetectorService
from app.prediction.prediction_service import PredictionService
from app.services.alert_service import AlertService
from app.repositories.observation_repo import get_repository
from app.repositories.evidence_repo import get_evidence_repository

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])

def get_agent_service() -> GeminiAgentService:
    obs_repo = get_repository()
    ev_repo = get_evidence_repository()
    detector = HotspotDetectorService(obs_repo, ev_repo)
    prediction = PredictionService(detector, obs_repo)
    alert_service = AlertService(detector, prediction)
    tools = VayuNetTools(detector, prediction, alert_service, obs_repo)
    return GeminiAgentService(tools)

@router.post("/chat", response_model=AgentChatResponse)
def chat_with_agent(payload: AgentChatRequest, agent: GeminiAgentService = Depends(get_agent_service)):
    try:
        result = agent.process_query(payload.message, payload.language)
        return AgentChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
