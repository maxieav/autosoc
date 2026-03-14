from __future__ import annotations
import logging
from abc import ABC, abstractmethod
from src.domain.entities.case import Case
from src.domain.value_objects.channel_capability import NotificationType

logger = logging.getLogger(__name__)


class INotificationSender(ABC):
    """Abstract interface for sending notifications via a channel."""

    @abstractmethod
    async def send_notification(
        self,
        recipient: str,
        subject: str,
        body: str,
        thread_id: str | None = None,
    ) -> str: ...


class NotificationService:
    def __init__(self, channels: list[INotificationSender]) -> None:
        self._channels = channels

    async def notify(
        self,
        case: Case,
        notification_type: NotificationType,
        recipients: list[str],
    ) -> None:
        subject_map = {
            NotificationType.CASE_CREATED: f"[AutoSOC] New Case: {case.title}",
            NotificationType.CASE_UPDATED: f"[AutoSOC] Case Updated: {case.title}",
            NotificationType.CASE_CLOSED: f"[AutoSOC] Case Closed: {case.title}",
        }
        subject = subject_map.get(notification_type, f"[AutoSOC] Case: {case.title}")
        body = (
            f"Case ID: {case.id}\n"
            f"Title: {case.title}\n"
            f"Status: {case.status.value}\n"
            f"Priority: {case.priority.value}\n"
            f"Description: {case.description}\n"
        )
        if case.ai_analysis:
            body += f"\nAI Analysis: {case.ai_analysis}"

        for channel in self._channels:
            for recipient in recipients:
                try:
                    await channel.send_notification(
                        recipient=recipient,
                        subject=subject,
                        body=body,
                    )
                    case.notifications_sent.append(f"{notification_type.value}:{recipient}")
                except Exception:
                    logger.exception(
                        "Failed to send %s notification to %s", notification_type.value, recipient
                    )
