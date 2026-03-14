from __future__ import annotations
from datetime import datetime, timezone
from uuid import uuid4
from src.domain.entities.client_tenant import ClientTenant
from src.domain.interfaces.client_tenant_repository import IClientTenantRepository
from src.application.dtos.tenant_dtos import CreateTenantDTO, TenantResponseDTO


def _to_response(tenant: ClientTenant) -> TenantResponseDTO:
    return TenantResponseDTO(
        id=tenant.id,
        name=tenant.name,
        active=tenant.active,
        system_connectors=tenant.system_connectors,
        communication_channels=tenant.communication_channels,
        created_at=tenant.created_at,
        updated_at=tenant.updated_at,
    )


class CreateTenantUseCase:
    def __init__(self, tenant_repo: IClientTenantRepository) -> None:
        self._repo = tenant_repo

    async def execute(self, dto: CreateTenantDTO) -> TenantResponseDTO:
        now = datetime.now(timezone.utc)
        tenant = ClientTenant(
            id=uuid4(),
            name=dto.name,
            active=dto.active,
            system_connectors=dto.system_connectors,
            communication_channels=dto.communication_channels,
            created_at=now,
            updated_at=now,
        )
        saved = await self._repo.save(tenant)
        return _to_response(saved)
