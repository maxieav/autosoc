from __future__ import annotations
from datetime import datetime, timezone
from uuid import UUID
from src.domain.interfaces.case_repository import ICaseRepository
from src.application.dtos.case_dtos import UpdateCaseDTO, CaseResponseDTO


def _to_response(case) -> CaseResponseDTO:
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


class UpdateCaseUseCase:
    def __init__(self, case_repo: ICaseRepository) -> None:
        self._repo = case_repo

    async def execute(self, case_id: UUID, dto: UpdateCaseDTO) -> CaseResponseDTO:
        case = await self._repo.get_by_id(case_id)
        if case is None:
            raise ValueError(f"Case {case_id} not found")
        if dto.title is not None:
            case.title = dto.title
        if dto.description is not None:
            case.description = dto.description
        if dto.priority is not None:
            case.priority = dto.priority
        if dto.assigned_to is not None:
            case.assigned_to = dto.assigned_to
        if dto.ai_analysis is not None:
            case.ai_analysis = dto.ai_analysis
        case.updated_at = datetime.now(timezone.utc)
        updated = await self._repo.update(case)
        return _to_response(updated)
