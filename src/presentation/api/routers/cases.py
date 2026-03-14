from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from src.application.dtos.case_dtos import CreateCaseDTO, UpdateCaseDTO, CaseResponseDTO
from src.application.use_cases.cases.create_case import CreateCaseUseCase
from src.application.use_cases.cases.update_case import UpdateCaseUseCase
from src.application.use_cases.cases.close_case import CloseCaseUseCase
from src.application.use_cases.cases.reopen_case import ReopenCaseUseCase
from src.application.use_cases.cases.assign_case import AssignCaseUseCase
from src.application.use_cases.cases.get_case import GetCaseUseCase
from src.application.use_cases.cases.list_cases import ListCasesUseCase
from src.presentation.api.dependencies import (
    get_create_case_use_case,
    get_update_case_use_case,
    get_close_case_use_case,
    get_reopen_case_use_case,
    get_assign_case_use_case,
    get_get_case_use_case,
    get_list_cases_use_case,
)
from src.presentation.api.schemas.case_schemas import AssignCaseRequest

router = APIRouter()


@router.post("/", response_model=CaseResponseDTO, status_code=201)
async def create_case(
    dto: CreateCaseDTO,
    use_case: CreateCaseUseCase = Depends(get_create_case_use_case),
) -> CaseResponseDTO:
    return await use_case.execute(dto)


@router.get("/", response_model=list[CaseResponseDTO])
async def list_cases(
    tenant_id: UUID,
    skip: int = 0,
    limit: int = 100,
    use_case: ListCasesUseCase = Depends(get_list_cases_use_case),
) -> list[CaseResponseDTO]:
    return await use_case.execute(tenant_id, skip=skip, limit=limit)


@router.get("/{case_id}", response_model=CaseResponseDTO)
async def get_case(
    case_id: UUID,
    use_case: GetCaseUseCase = Depends(get_get_case_use_case),
) -> CaseResponseDTO:
    try:
        return await use_case.execute(case_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{case_id}", response_model=CaseResponseDTO)
async def update_case(
    case_id: UUID,
    dto: UpdateCaseDTO,
    use_case: UpdateCaseUseCase = Depends(get_update_case_use_case),
) -> CaseResponseDTO:
    try:
        return await use_case.execute(case_id, dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{case_id}/close", response_model=CaseResponseDTO)
async def close_case(
    case_id: UUID,
    use_case: CloseCaseUseCase = Depends(get_close_case_use_case),
) -> CaseResponseDTO:
    try:
        return await use_case.execute(case_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{case_id}/reopen", response_model=CaseResponseDTO)
async def reopen_case(
    case_id: UUID,
    use_case: ReopenCaseUseCase = Depends(get_reopen_case_use_case),
) -> CaseResponseDTO:
    try:
        return await use_case.execute(case_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{case_id}/assign", response_model=CaseResponseDTO)
async def assign_case(
    case_id: UUID,
    body: AssignCaseRequest,
    use_case: AssignCaseUseCase = Depends(get_assign_case_use_case),
) -> CaseResponseDTO:
    try:
        return await use_case.execute(case_id, body.assigned_to)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
