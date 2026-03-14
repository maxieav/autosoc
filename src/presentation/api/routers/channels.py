from __future__ import annotations
from fastapi import APIRouter, Depends
from src.application.dtos.connector_dtos import RegisterCommunicationChannelDTO, CommunicationChannelResponseDTO
from src.application.use_cases.connectors.register_communication_channel import RegisterCommunicationChannelUseCase
from src.presentation.api.dependencies import get_register_communication_channel_use_case

router = APIRouter()


@router.post("/", response_model=CommunicationChannelResponseDTO, status_code=201)
async def register_communication_channel(
    dto: RegisterCommunicationChannelDTO,
    use_case: RegisterCommunicationChannelUseCase = Depends(get_register_communication_channel_use_case),
) -> CommunicationChannelResponseDTO:
    return await use_case.execute(dto)
