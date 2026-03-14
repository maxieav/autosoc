from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from src.domain.value_objects.channel_type import ChannelType
from src.domain.value_objects.channel_capability import ChannelCapability


@dataclass
class CommunicationChannel:
    id: UUID
    name: str
    channel_type: ChannelType
    config: dict[str, str]
    active: bool
    created_at: datetime
    updated_at: datetime
    capabilities: list[ChannelCapability] = field(default_factory=list)
