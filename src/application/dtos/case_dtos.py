from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from src.domain.value_objects.case_status import CaseStatus
from src.domain.value_objects.case_priority import CasePriority


class CreateCaseDTO(BaseModel):
    title: str
    description: str
    priority: CasePriority
    client_tenant_id: UUID
    assigned_to: str | None = None


class UpdateCaseDTO(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: CasePriority | None = None
    assigned_to: str | None = None
    ai_analysis: str | None = None


class CaseResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: str
    status: CaseStatus
    priority: CasePriority
    client_tenant_id: UUID
    assigned_to: str | None
    external_ids: dict[str, str]
    ai_analysis: str | None
    notifications_sent: list[str]
    created_at: datetime
    updated_at: datetime
