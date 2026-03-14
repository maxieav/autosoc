from abc import ABC, abstractmethod
from uuid import UUID
from src.domain.entities.client_tenant import ClientTenant


class IClientTenantRepository(ABC):
    @abstractmethod
    async def get_by_id(self, tenant_id: UUID) -> ClientTenant | None: ...

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[ClientTenant]: ...

    @abstractmethod
    async def save(self, tenant: ClientTenant) -> ClientTenant: ...

    @abstractmethod
    async def update(self, tenant: ClientTenant) -> ClientTenant: ...

    @abstractmethod
    async def delete(self, tenant_id: UUID) -> None: ...
