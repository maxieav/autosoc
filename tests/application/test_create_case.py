import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4
from src.domain.entities.case import Case
from src.domain.value_objects.case_status import CaseStatus
from src.domain.value_objects.case_priority import CasePriority
from src.application.dtos.case_dtos import CreateCaseDTO
from src.application.use_cases.cases.create_case import CreateCaseUseCase
from src.application.services.ai_engine_service import AIAnalysisResult


@pytest.fixture
def mock_ai_engine():
    ai = AsyncMock()
    ai.analyze_case.return_value = AIAnalysisResult(
        summary="Suspicious login activity detected",
        threat_level="high",
        confidence_score=0.85,
        recommended_actions=["Investigate", "Block IP"],
        similar_cases=[],
    )
    return ai


@pytest.fixture
def mock_case_repo():
    repo = AsyncMock()

    async def save_side_effect(case: Case) -> Case:
        return case

    repo.save.side_effect = save_side_effect
    return repo


@pytest.mark.asyncio
async def test_create_case_sets_open_status(mock_case_repo, mock_ai_engine):
    use_case = CreateCaseUseCase(mock_case_repo, mock_ai_engine)
    dto = CreateCaseDTO(
        title="Brute Force Attack",
        description="Multiple failed login attempts",
        priority=CasePriority.HIGH,
        client_tenant_id=uuid4(),
    )
    result = await use_case.execute(dto)
    assert result.status == CaseStatus.OPEN
    assert result.title == "Brute Force Attack"
    assert result.priority == CasePriority.HIGH


@pytest.mark.asyncio
async def test_create_case_calls_ai_analysis(mock_case_repo, mock_ai_engine):
    use_case = CreateCaseUseCase(mock_case_repo, mock_ai_engine)
    dto = CreateCaseDTO(
        title="Ransomware Detected",
        description="File encryption detected on endpoint",
        priority=CasePriority.CRITICAL,
        client_tenant_id=uuid4(),
    )
    result = await use_case.execute(dto)
    mock_ai_engine.analyze_case.assert_called_once()
    assert result.ai_analysis == "Suspicious login activity detected"


@pytest.mark.asyncio
async def test_create_case_saves_to_repo(mock_case_repo, mock_ai_engine):
    use_case = CreateCaseUseCase(mock_case_repo, mock_ai_engine)
    dto = CreateCaseDTO(
        title="Data Exfiltration",
        description="Unusual outbound traffic",
        priority=CasePriority.CRITICAL,
        client_tenant_id=uuid4(),
    )
    await use_case.execute(dto)
    mock_case_repo.save.assert_called_once()
