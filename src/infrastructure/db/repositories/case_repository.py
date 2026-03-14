from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.case import Case
from src.domain.interfaces.case_repository import ICaseRepository
from src.domain.value_objects.case_status import CaseStatus
from src.domain.value_objects.case_priority import CasePriority
from src.infrastructure.db.models import CaseModel


def _to_entity(model: CaseModel) -> Case:
    return Case(
        id=model.id,
        title=model.title,
        description=model.description,
        status=CaseStatus(model.status),
        priority=CasePriority(model.priority),
        client_tenant_id=model.client_tenant_id,
        assigned_to=model.assigned_to,
        external_ids=model.external_ids or {},
        ai_analysis=model.ai_analysis,
        notifications_sent=model.notifications_sent or [],
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_model(case: Case) -> CaseModel:
    return CaseModel(
        id=case.id,
        title=case.title,
        description=case.description,
        status=case.status.value,
        priority=case.priority.value,
        client_tenant_id=case.client_tenant_id,
        assigned_to=case.assigned_to,
        external_ids=case.external_ids,
        ai_analysis=case.ai_analysis,
        notifications_sent=case.notifications_sent,
        created_at=case.created_at,
        updated_at=case.updated_at,
    )


class CaseRepository(ICaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, case_id: UUID) -> Case | None:
        result = await self._session.get(CaseModel, case_id)
        return _to_entity(result) if result else None

    async def list_by_tenant(self, tenant_id: UUID, skip: int = 0, limit: int = 100) -> list[Case]:
        stmt = (
            select(CaseModel)
            .where(CaseModel.client_tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, case: Case) -> Case:
        model = _to_model(case)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return _to_entity(model)

    async def update(self, case: Case) -> Case:
        model = await self._session.get(CaseModel, case.id)
        if model is None:
            raise ValueError(f"Case {case.id} not found")
        model.title = case.title
        model.description = case.description
        model.status = case.status.value
        model.priority = case.priority.value
        model.assigned_to = case.assigned_to
        model.external_ids = case.external_ids
        model.ai_analysis = case.ai_analysis
        model.notifications_sent = case.notifications_sent
        model.updated_at = case.updated_at
        await self._session.commit()
        await self._session.refresh(model)
        return _to_entity(model)

    async def delete(self, case_id: UUID) -> None:
        model = await self._session.get(CaseModel, case_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()
