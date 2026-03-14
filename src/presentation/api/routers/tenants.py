from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from src.application.dtos.tenant_dtos import CreateTenantDTO, UpdateTenantDTO, TenantResponseDTO
from src.application.use_cases.tenants.create_tenant import CreateTenantUseCase
from src.application.use_cases.tenants.update_tenant import UpdateTenantUseCase
from src.application.use_cases.tenants.get_tenant import GetTenantUseCase
from src.application.use_cases.tenants.list_tenants import ListTenantsUseCase
from src.presentation.api.dependencies import (
    get_create_tenant_use_case,
    get_update_tenant_use_case,
    get_get_tenant_use_case,
    get_list_tenants_use_case,
)

router = APIRouter()


@router.post("/", response_model=TenantResponseDTO, status_code=201)
async def create_tenant(
    dto: CreateTenantDTO,
    use_case: CreateTenantUseCase = Depends(get_create_tenant_use_case),
) -> TenantResponseDTO:
    return await use_case.execute(dto)


@router.get("/", response_model=list[TenantResponseDTO])
async def list_tenants(
    skip: int = 0,
    limit: int = 100,
    use_case: ListTenantsUseCase = Depends(get_list_tenants_use_case),
) -> list[TenantResponseDTO]:
    return await use_case.execute(skip=skip, limit=limit)


@router.get("/{tenant_id}", response_model=TenantResponseDTO)
async def get_tenant(
    tenant_id: UUID,
    use_case: GetTenantUseCase = Depends(get_get_tenant_use_case),
) -> TenantResponseDTO:
    try:
        return await use_case.execute(tenant_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{tenant_id}", response_model=TenantResponseDTO)
async def update_tenant(
    tenant_id: UUID,
    dto: UpdateTenantDTO,
    use_case: UpdateTenantUseCase = Depends(get_update_tenant_use_case),
) -> TenantResponseDTO:
    try:
        return await use_case.execute(tenant_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
