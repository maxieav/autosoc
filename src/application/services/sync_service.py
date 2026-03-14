from __future__ import annotations
import logging
from src.domain.entities.case import Case
from src.domain.interfaces.case_repository import ICaseRepository
from src.infrastructure.connectors.base import BaseSystemConnector

logger = logging.getLogger(__name__)


class SyncService:
    def __init__(
        self,
        case_repo: ICaseRepository,
        connectors: list[BaseSystemConnector],
        connector_ids: list[str],
    ) -> None:
        self._case_repo = case_repo
        self._connectors = connectors
        self._connector_ids = connector_ids

    async def sync_case_to_external(self, case: Case) -> Case:
        for connector, connector_id in zip(self._connectors, self._connector_ids):
            external_id = case.external_ids.get(connector_id)
            try:
                if external_id:
                    await connector.update_case(external_id, case)
                else:
                    new_external_id = await connector.create_case(case)
                    case.external_ids[connector_id] = new_external_id
            except Exception:
                logger.exception("Failed to sync case %s to connector %s", case.id, connector_id)
        updated = await self._case_repo.update(case)
        return updated
