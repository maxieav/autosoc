from __future__ import annotations
from datetime import datetime, timezone
from uuid import uuid4, UUID
from src.domain.entities.case import Case
from src.domain.value_objects.case_status import CaseStatus
from src.domain.value_objects.case_priority import CasePriority
from src.domain.interfaces.case_repository import ICaseRepository
from src.application.services.ai_engine_service import IAIEngineService
from src.application.services.notification_service import INotificationSender
from src.application.dtos.case_dtos import CaseResponseDTO


def _to_response(case: Case) -> CaseResponseDTO:
    return CaseResponseDTO(
        id=case.id,
        title=case.title,
        description=case.description,
        status=case.status,
        priority=case.priority,
        client_tenant_id=case.client_tenant_id,
        assigned_to=case.assigned_to,
        external_ids=case.external_ids,
        ai_analysis=case.ai_analysis,
        notifications_sent=case.notifications_sent,
        created_at=case.created_at,
        updated_at=case.updated_at,
    )


class HandleInboundMessageUseCase:
    def __init__(
        self,
        case_repo: ICaseRepository,
        ai_engine: IAIEngineService,
        channel: INotificationSender,
    ) -> None:
        self._repo = case_repo
        self._ai = ai_engine
        self._channel = channel

    async def execute(
        self,
        sender: str,
        subject: str,
        body: str,
        tenant_id: UUID,
    ) -> CaseResponseDTO:
        now = datetime.now(timezone.utc)
        case = Case(
            id=uuid4(),
            title=subject,
            description=body,
            status=CaseStatus.OPEN,
            priority=CasePriority.MEDIUM,
            client_tenant_id=tenant_id,
            assigned_to=None,
            created_at=now,
            updated_at=now,
        )
        analysis = await self._ai.analyze_case(case)
        case.ai_analysis = analysis.summary
        saved = await self._repo.save(case)
        await self._channel.send_notification(
            recipient=sender,
            subject=f"Case created: {saved.id}",
            body=f"Your case has been created with ID {saved.id}.\n\nAI Analysis: {saved.ai_analysis}",
        )
        return _to_response(saved)
