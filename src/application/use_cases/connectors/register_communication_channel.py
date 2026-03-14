from __future__ import annotations
from datetime import datetime, timezone
from uuid import uuid4
from src.domain.entities.communication_channel import CommunicationChannel
from src.domain.interfaces.communication_channel_repository import ICommunicationChannelRepository
from src.application.dtos.connector_dtos import RegisterCommunicationChannelDTO, CommunicationChannelResponseDTO


def _to_response(channel: CommunicationChannel) -> CommunicationChannelResponseDTO:
    return CommunicationChannelResponseDTO(
        id=channel.id,
        name=channel.name,
        channel_type=channel.channel_type,
        config=channel.config,
        capabilities=channel.capabilities,
        active=channel.active,
        created_at=channel.created_at,
        updated_at=channel.updated_at,
    )


class RegisterCommunicationChannelUseCase:
    def __init__(self, channel_repo: ICommunicationChannelRepository) -> None:
        self._repo = channel_repo

    async def execute(self, dto: RegisterCommunicationChannelDTO) -> CommunicationChannelResponseDTO:
        now = datetime.now(timezone.utc)
        channel = CommunicationChannel(
            id=uuid4(),
            name=dto.name,
            channel_type=dto.channel_type,
            config=dto.config,
            capabilities=dto.capabilities,
            active=dto.active,
            created_at=now,
            updated_at=now,
        )
        saved = await self._repo.save(channel)
        return _to_response(saved)
