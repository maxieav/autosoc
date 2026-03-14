from __future__ import annotations
import httpx
from src.domain.entities.case import Case
from src.infrastructure.connectors.base import BaseSystemConnector


class JiraConnector(BaseSystemConnector):
    def __init__(self, base_url: str, credentials: dict[str, str]) -> None:
        self._base_url = base_url
        self._credentials = credentials

    async def create_case(self, case: Case) -> str:
        project_key = self._credentials.get("project_key", "SOC")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/rest/api/3/issue",
                json={
                    "fields": {
                        "project": {"key": project_key},
                        "summary": case.title,
                        "description": {
                            "type": "doc",
                            "version": 1,
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [{"type": "text", "text": case.description}],
                                }
                            ],
                        },
                        "issuetype": {"name": "Task"},
                    }
                },
                headers={"Content-Type": "application/json"},
                auth=(
                    self._credentials.get("email", ""),
                    self._credentials.get("api_token", ""),
                ),
            )
            response.raise_for_status()
            data = response.json()
            return data["key"]

    async def update_case(self, external_id: str, case: Case) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self._base_url}/rest/api/3/issue/{external_id}",
                json={"fields": {"summary": case.title}},
                headers={"Content-Type": "application/json"},
                auth=(
                    self._credentials.get("email", ""),
                    self._credentials.get("api_token", ""),
                ),
            )
            response.raise_for_status()

    async def close_case(self, external_id: str) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/rest/api/3/issue/{external_id}/transitions",
                json={"transition": {"id": "31"}},
                headers={"Content-Type": "application/json"},
                auth=(
                    self._credentials.get("email", ""),
                    self._credentials.get("api_token", ""),
                ),
            )
            response.raise_for_status()
