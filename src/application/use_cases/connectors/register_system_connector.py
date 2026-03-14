from __future__ import annotations
from datetime import datetime, timezone
from uuid import uuid4
from src.domain.entities.system_connector import SystemConnector
from src.domain.interfaces.system_connector_repository import ISystemConnectorRepository
from src.application.dtos.connector_dtos import RegisterSystemConnectorDTO, SystemConnectorResponseDTO


def _to_response(connector: SystemConnector) -> SystemConnectorResponseDTO:
    return SystemConnectorResponseDTO(
        id=connector.id,
        name=connector.name,
        connector_type=connector.connector_type,
        base_url=connector.base_url,
        capabilities=connector.capabilities,
        active=connector.active,
        created_at=connector.created_at,
        updated_at=connector.updated_at,
    )


class RegisterSystemConnectorUseCase:
    def __init__(self, connector_repo: ISystemConnectorRepository) -> None:
        self._repo = connector_repo

    async def execute(self, dto: RegisterSystemConnectorDTO) -> SystemConnectorResponseDTO:
        now = datetime.now(timezone.utc)
        connector = SystemConnector(
            id=uuid4(),
            name=dto.name,
            connector_type=dto.connector_type,
            base_url=dto.base_url,
            credentials=dto.credentials,
            capabilities=dto.capabilities,
            active=dto.active,
            created_at=now,
            updated_at=now,
        )
        saved = await self._repo.save(connector)
        return _to_response(saved)
