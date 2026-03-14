from abc import ABC, abstractmethod
from uuid import UUID
from src.domain.entities.case import Case


class ICaseRepository(ABC):
    @abstractmethod
    async def get_by_id(self, case_id: UUID) -> Case | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: UUID, skip: int = 0, limit: int = 100) -> list[Case]: ...

    @abstractmethod
    async def save(self, case: Case) -> Case: ...

    @abstractmethod
    async def update(self, case: Case) -> Case: ...

    @abstractmethod
    async def delete(self, case_id: UUID) -> None: ...
