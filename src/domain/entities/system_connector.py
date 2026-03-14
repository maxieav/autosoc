from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from src.domain.value_objects.connector_type import ConnectorType
from src.domain.value_objects.system_capability import SystemCapability


@dataclass
class SystemConnector:
    id: UUID
    name: str
    connector_type: ConnectorType
    base_url: str
    credentials: dict[str, str]
    active: bool
    created_at: datetime
    updated_at: datetime
    capabilities: list[SystemCapability] = field(default_factory=list)
