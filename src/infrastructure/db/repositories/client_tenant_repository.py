from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.client_tenant import ClientTenant
from src.domain.interfaces.client_tenant_repository import IClientTenantRepository
from src.infrastructure.db.models import ClientTenantModel


def _to_entity(model: ClientTenantModel) -> ClientTenant:
    return ClientTenant(
        id=model.id,
        name=model.name,
        active=model.active,
        system_connectors=model.system_connectors or [],
        communication_channels=model.communication_channels or [],
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_model(tenant: ClientTenant) -> ClientTenantModel:
    return ClientTenantModel(
        id=tenant.id,
        name=tenant.name,
        active=tenant.active,
        system_connectors=tenant.system_connectors,
        communication_channels=tenant.communication_channels,
        created_at=tenant.created_at,
        updated_at=tenant.updated_at,
    )


class ClientTenantRepository(IClientTenantRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, tenant_id: UUID) -> ClientTenant | None:
        result = await self._session.get(ClientTenantModel, tenant_id)
        return _to_entity(result) if result else None

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[ClientTenant]:
        stmt = select(ClientTenantModel).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, tenant: ClientTenant) -> ClientTenant:
        model = _to_model(tenant)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return _to_entity(model)

    async def update(self, tenant: ClientTenant) -> ClientTenant:
        model = await self._session.get(ClientTenantModel, tenant.id)
        if model is None:
            raise ValueError(f"Tenant {tenant.id} not found")
        model.name = tenant.name
        model.active = tenant.active
        model.system_connectors = tenant.system_connectors
        model.communication_channels = tenant.communication_channels
        model.updated_at = tenant.updated_at
        await self._session.commit()
        await self._session.refresh(model)
        return _to_entity(model)

    async def delete(self, tenant_id: UUID) -> None:
        model = await self._session.get(ClientTenantModel, tenant_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()
