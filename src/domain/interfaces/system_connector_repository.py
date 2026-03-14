from abc import ABC, abstractmethod
from uuid import UUID
from src.domain.entities.system_connector import SystemConnector


class ISystemConnectorRepository(ABC):
    @abstractmethod
    async def get_by_id(self, connector_id: UUID) -> SystemConnector | None: ...

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[SystemConnector]: ...

    @abstractmethod
    async def save(self, connector: SystemConnector) -> SystemConnector: ...

    @abstractmethod
    async def update(self, connector: SystemConnector) -> SystemConnector: ...

    @abstractmethod
    async def delete(self, connector_id: UUID) -> None: ...
