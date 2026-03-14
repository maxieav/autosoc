from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class ClientTenant:
    id: UUID
    name: str
    active: bool
    created_at: datetime
    updated_at: datetime
    system_connectors: list[dict] = field(default_factory=list)
    communication_channels: list[dict] = field(default_factory=list)
