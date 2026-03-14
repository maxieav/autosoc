from abc import ABC, abstractmethod
from src.domain.entities.case import Case
from src.application.services.notification_service import INotificationSender


class BaseSystemConnector(ABC):
    @abstractmethod
    async def create_case(self, case: Case) -> str: ...

    @abstractmethod
    async def update_case(self, external_id: str, case: Case) -> None: ...

    @abstractmethod
    async def close_case(self, external_id: str) -> None: ...


class BaseCommunicationChannel(INotificationSender, ABC):
    @abstractmethod
    async def send_notification(
        self,
        recipient: str,
        subject: str,
        body: str,
        thread_id: str | None = None,
    ) -> str: ...
