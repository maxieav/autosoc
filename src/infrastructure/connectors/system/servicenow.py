from __future__ import annotations
import httpx
from src.domain.entities.case import Case
from src.infrastructure.connectors.base import BaseSystemConnector


class ServiceNowConnector(BaseSystemConnector):
    def __init__(self, base_url: str, credentials: dict[str, str]) -> None:
        self._base_url = base_url
        self._credentials = credentials

    async def create_case(self, case: Case) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/api/now/table/incident",
                json={
                    "short_description": case.title,
                    "description": case.description,
                    "urgency": "2",
                },
                auth=(
                    self._credentials.get("username", ""),
                    self._credentials.get("password", ""),
                ),
            )
            response.raise_for_status()
            data = response.json()
            return data["result"]["sys_id"]

    async def update_case(self, external_id: str, case: Case) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self._base_url}/api/now/table/incident/{external_id}",
                json={
                    "short_description": case.title,
                    "description": case.description,
                },
                auth=(
                    self._credentials.get("username", ""),
                    self._credentials.get("password", ""),
                ),
            )
            response.raise_for_status()

    async def close_case(self, external_id: str) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self._base_url}/api/now/table/incident/{external_id}",
                json={"state": "7"},
                auth=(
                    self._credentials.get("username", ""),
                    self._credentials.get("password", ""),
                ),
            )
            response.raise_for_status()
