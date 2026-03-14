from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from src.domain.entities.case import Case


@dataclass
class AIAnalysisResult:
    summary: str
    threat_level: str
    confidence_score: float
    recommended_actions: list[str] = field(default_factory=list)
    similar_cases: list[str] = field(default_factory=list)


class IAIEngineService(ABC):
    @abstractmethod
    async def analyze_case(self, case: Case) -> AIAnalysisResult: ...
