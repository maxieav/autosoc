from __future__ import annotations
from uuid import UUID
from src.domain.interfaces.case_repository import ICaseRepository
from src.application.dtos.case_dtos import CaseResponseDTO


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


class ListCasesUseCase:
    def __init__(self, case_repo: ICaseRepository) -> None:
        self._repo = case_repo

    async def execute(self, tenant_id: UUID, skip: int = 0, limit: int = 100) -> list[CaseResponseDTO]:
        cases = await self._repo.list_by_tenant(tenant_id, skip=skip, limit=limit)
        return [_to_response(c) for c in cases]
