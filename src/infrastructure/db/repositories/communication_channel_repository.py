from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.communication_channel import CommunicationChannel
from src.domain.interfaces.communication_channel_repository import ICommunicationChannelRepository
from src.domain.value_objects.channel_type import ChannelType
from src.domain.value_objects.channel_capability import ChannelCapability
from src.infrastructure.db.models import CommunicationChannelModel


def _to_entity(model: CommunicationChannelModel) -> CommunicationChannel:
    return CommunicationChannel(
        id=model.id,
        name=model.name,
        channel_type=ChannelType(model.channel_type),
        config=model.config or {},
        capabilities=[ChannelCapability(c) for c in (model.capabilities or [])],
        active=model.active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_model(channel: CommunicationChannel) -> CommunicationChannelModel:
    return CommunicationChannelModel(
        id=channel.id,
        name=channel.name,
        channel_type=channel.channel_type.value,
        config=channel.config,
        capabilities=[c.value for c in channel.capabilities],
        active=channel.active,
        created_at=channel.created_at,
        updated_at=channel.updated_at,
    )


class CommunicationChannelRepository(ICommunicationChannelRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, channel_id: UUID) -> CommunicationChannel | None:
        result = await self._session.get(CommunicationChannelModel, channel_id)
        return _to_entity(result) if result else None

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[CommunicationChannel]:
        stmt = select(CommunicationChannelModel).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return [_to_entity(m) for m in result.scalars().all()]

    async def save(self, channel: CommunicationChannel) -> CommunicationChannel:
        model = _to_model(channel)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return _to_entity(model)

    async def update(self, channel: CommunicationChannel) -> CommunicationChannel:
        model = await self._session.get(CommunicationChannelModel, channel.id)
        if model is None:
            raise ValueError(f"CommunicationChannel {channel.id} not found")
        model.name = channel.name
        model.channel_type = channel.channel_type.value
        model.config = channel.config
        model.capabilities = [c.value for c in channel.capabilities]
        model.active = channel.active
        model.updated_at = channel.updated_at
        await self._session.commit()
        await self._session.refresh(model)
        return _to_entity(model)

    async def delete(self, channel_id: UUID) -> None:
        model = await self._session.get(CommunicationChannelModel, channel_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()
