from __future__ import annotations
import logging
import httpx
from src.infrastructure.connectors.base import BaseCommunicationChannel

logger = logging.getLogger(__name__)


class SlackChannel(BaseCommunicationChannel):
    def __init__(self, config: dict[str, str]) -> None:
        self._config = config

    async def send_notification(
        self,
        recipient: str,
        subject: str,
        body: str,
        thread_id: str | None = None,
    ) -> str:
        webhook_url = self._config.get("webhook_url", "")
        if not webhook_url:
            logger.warning("Slack webhook_url is not configured; notification to %s skipped", recipient)
            return thread_id or ""

        payload: dict = {
            "channel": recipient,
            "text": f"*{subject}*\n{body}",
        }
        if thread_id:
            payload["thread_ts"] = thread_id

        async with httpx.AsyncClient() as client:
            response = await client.post(webhook_url, json=payload)
            response.raise_for_status()
        return thread_id or ""
