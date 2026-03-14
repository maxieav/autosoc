from __future__ import annotations
from uuid import UUID
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


class GetTenantUseCase:
    def __init__(self, tenant_repo: IClientTenantRepository) -> None:
        self._repo = tenant_repo

    async def execute(self, tenant_id: UUID) -> TenantResponseDTO:
        tenant = await self._repo.get_by_id(tenant_id)
        if tenant is None:
            raise ValueError(f"Tenant {tenant_id} not found")
        return _to_response(tenant)
