from __future__ import annotations
from fastapi import APIRouter, Depends
from src.application.dtos.connector_dtos import RegisterSystemConnectorDTO, SystemConnectorResponseDTO
from src.application.use_cases.connectors.register_system_connector import RegisterSystemConnectorUseCase
from src.presentation.api.dependencies import get_register_system_connector_use_case

router = APIRouter()


@router.post("/", response_model=SystemConnectorResponseDTO, status_code=201)
async def register_system_connector(
    dto: RegisterSystemConnectorDTO,
    use_case: RegisterSystemConnectorUseCase = Depends(get_register_system_connector_use_case),
) -> SystemConnectorResponseDTO:
    return await use_case.execute(dto)
