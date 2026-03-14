from __future__ import annotations
from datetime import datetime, timezone
from uuid import UUID
from src.domain.interfaces.client_tenant_repository import IClientTenantRepository
from src.application.dtos.tenant_dtos import UpdateTenantDTO, TenantResponseDTO


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


class UpdateTenantUseCase:
    def __init__(self, tenant_repo: IClientTenantRepository) -> None:
        self._repo = tenant_repo

    async def execute(self, tenant_id: UUID, dto: UpdateTenantDTO) -> TenantResponseDTO:
        tenant = await self._repo.get_by_id(tenant_id)
        if tenant is None:
            raise ValueError(f"Tenant {tenant_id} not found")
        if dto.name is not None:
            tenant.name = dto.name
        if dto.active is not None:
            tenant.active = dto.active
        if dto.system_connectors is not None:
            tenant.system_connectors = dto.system_connectors
        if dto.communication_channels is not None:
            tenant.communication_channels = dto.communication_channels
        tenant.updated_at = datetime.now(timezone.utc)
        updated = await self._repo.update(tenant)
        return _to_response(updated)
