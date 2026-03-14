from __future__ import annotations
from src.domain.interfaces.client_tenant_repository import IClientTenantRepository
from src.application.dtos.tenant_dtos import TenantResponseDTO


def _to_response(tenant) -> TenantResponseDTO:
    return TenantResponseDTO(
        id=tenant.id,
        name=tenant.name,
        active=tenant.active,
        system_connectors=tenant.system_connectors,
        communication_channels=tenant.communication_channels,
        created_at=tenant.created_at,
        updated_at=tenant.updated_at,
    )


class ListTenantsUseCase:
    def __init__(self, tenant_repo: IClientTenantRepository) -> None:
        self._repo = tenant_repo

    async def execute(self, skip: int = 0, limit: int = 100) -> list[TenantResponseDTO]:
        tenants = await self._repo.list_all(skip=skip, limit=limit)
        return [_to_response(t) for t in tenants]
