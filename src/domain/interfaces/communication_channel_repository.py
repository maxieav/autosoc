from abc import ABC, abstractmethod
from uuid import UUID
from src.domain.entities.communication_channel import CommunicationChannel


class ICommunicationChannelRepository(ABC):
    @abstractmethod
    async def get_by_id(self, channel_id: UUID) -> CommunicationChannel | None: ...

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[CommunicationChannel]: ...

    @abstractmethod
    async def save(self, channel: CommunicationChannel) -> CommunicationChannel: ...

    @abstractmethod
    async def update(self, channel: CommunicationChannel) -> CommunicationChannel: ...

    @abstractmethod
    async def delete(self, channel_id: UUID) -> None: ...
