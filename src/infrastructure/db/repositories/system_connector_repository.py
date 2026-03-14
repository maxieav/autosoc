from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.system_connector import SystemConnector
from src.domain.interfaces.system_connector_repository import ISystemConnectorRepository
from src.domain.value_objects.connector_type import ConnectorType
from src.domain.value_objects.system_capability import SystemCapability
from src.infrastructure.db.models import SystemConnectorModel


def _to_entity(model: SystemConnectorModel) -> SystemConnector:
    return SystemConnector(
        id=model.id,
        name=model.name,
        connector_type=ConnectorType(model.connector_type),
        base_url=model.base_url,
        credentials=model.credentials or {},
        capabilities=[SystemCapability(c) for c in (model.capabilities or [])],
        active=model.active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_model(connector: SystemConnector) -> SystemConnectorModel:
    return SystemConnectorModel(
        id=connector.id,
        name=connector.name,
        connector_type=connector.connector_type.value,
        base_url=connector.base_url,
        credentials=connector.credentials,
        capabilities=[c.value for c in connector.capabilities],
        active=connector.active,
        created_at=connector.created_at,
        updated_at=connector.updated_at,
    )


class SystemConnectorRepository(ISystemConnectorRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, connector_id: UUID) -> SystemConnector | None:
        result = await self._session.get(SystemConnectorModel, connector_id)
        return _to_entity(result) if result else None

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[SystemConnector]:
        stmt = select(SystemConnectorModel).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, connector: SystemConnector) -> SystemConnector:
        model = _to_model(connector)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return _to_entity(model)

    async def update(self, connector: SystemConnector) -> SystemConnector:
        model = await self._session.get(SystemConnectorModel, connector.id)
        if model is None:
            raise ValueError(f"SystemConnector {connector.id} not found")
        model.name = connector.name
        model.connector_type = connector.connector_type.value
        model.base_url = connector.base_url
        model.credentials = connector.credentials
        model.capabilities = [c.value for c in connector.capabilities]
        model.active = connector.active
        model.updated_at = connector.updated_at
        await self._session.commit()
        await self._session.refresh(model)
        return _to_entity(model)

    async def delete(self, connector_id: UUID) -> None:
        model = await self._session.get(SystemConnectorModel, connector_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()
