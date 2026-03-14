from __future__ import annotations
import json
import logging
import httpx
from src.application.services.ai_engine_service import IAIEngineService, AIAnalysisResult
from src.domain.entities.case import Case

logger = logging.getLogger(__name__)


class OllamaAIEngine(IAIEngineService):
    def __init__(self, base_url: str, model: str) -> None:
        self._base_url = base_url
        self._model = model

    async def analyze_case(self, case: Case) -> AIAnalysisResult:
        prompt = (
            f"Analyze this cybersecurity case and respond with JSON only:\n"
            f"Case: {case.title}\n"
            f"Description: {case.description}\n"
            f"Priority: {case.priority.value}\n\n"
            f'Respond with this exact JSON structure:\n'
            f'{{"summary": "...", "threat_level": "low|medium|high|critical", '
            f'"confidence_score": 0.0-1.0, "recommended_actions": ["..."], "similar_cases": ["..."]}}'
        )
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self._base_url}/api/generate",
                    json={"model": self._model, "prompt": prompt, "stream": False},
                )
                response.raise_for_status()
                data = response.json()
                result = json.loads(data["response"])
                return AIAnalysisResult(
                    summary=result.get("summary", ""),
                    threat_level=result.get("threat_level", "medium"),
                    confidence_score=float(result.get("confidence_score", 0.5)),
                    recommended_actions=result.get("recommended_actions", []),
                    similar_cases=result.get("similar_cases", []),
                )
        except Exception:
            logger.exception("AI analysis failed for case %s; returning fallback result", case.id)
            return AIAnalysisResult(
                summary=f"Case requires manual analysis: {case.title}",
                threat_level=case.priority.value,
                confidence_score=0.0,
                recommended_actions=["Manual review required"],
                similar_cases=[],
            )
