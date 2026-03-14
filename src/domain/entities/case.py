from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from src.domain.value_objects.case_status import CaseStatus
from src.domain.value_objects.case_priority import CasePriority


@dataclass
class Case:
    id: UUID
    title: str
    description: str
    status: CaseStatus
    priority: CasePriority
    client_tenant_id: UUID
    created_at: datetime
    updated_at: datetime
    assigned_to: str | None = None
    external_ids: dict[str, str] = field(default_factory=dict)
    ai_analysis: str | None = None
    notifications_sent: list[str] = field(default_factory=list)
