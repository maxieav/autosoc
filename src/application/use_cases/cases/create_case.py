from __future__ import annotations
from datetime import datetime, timezone
from uuid import uuid4
from src.domain.entities.case import Case
from src.domain.value_objects.case_status import CaseStatus
from src.domain.interfaces.case_repository import ICaseRepository
from src.application.dtos.case_dtos import CreateCaseDTO, CaseResponseDTO
from src.application.services.ai_engine_service import IAIEngineService


def _to_response(case: Case) -> CaseResponseDTO:
    return CaseResponseDTO(
        id=case.id,
        title=case.title,
        description=case.description,
        status=case.status,
        priority=case.priority,
        client_tenant_id=case.client_tenant_id,
        assigned_to=case.assigned_to,
        external_ids=case.external_ids,
        ai_analysis=case.ai_analysis,
        notifications_sent=case.notifications_sent,
        created_at=case.created_at,
        updated_at=case.updated_at,
    )


class CreateCaseUseCase:
    def __init__(self, case_repo: ICaseRepository, ai_engine: IAIEngineService) -> None:
        self._repo = case_repo
        self._ai = ai_engine

    async def execute(self, dto: CreateCaseDTO) -> CaseResponseDTO:
        now = datetime.now(timezone.utc)
        case = Case(
            id=uuid4(),
            title=dto.title,
            description=dto.description,
            status=CaseStatus.OPEN,
            priority=dto.priority,
            client_tenant_id=dto.client_tenant_id,
            assigned_to=dto.assigned_to,
            created_at=now,
            updated_at=now,
        )
        analysis = await self._ai.analyze_case(case)
        case.ai_analysis = analysis.summary
        saved = await self._repo.save(case)
        return _to_response(saved)
