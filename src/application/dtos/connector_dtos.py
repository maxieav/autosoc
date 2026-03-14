from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from src.domain.value_objects.connector_type import ConnectorType
from src.domain.value_objects.channel_type import ChannelType
from src.domain.value_objects.system_capability import SystemCapability
from src.domain.value_objects.channel_capability import ChannelCapability


class RegisterSystemConnectorDTO(BaseModel):
    name: str
    connector_type: ConnectorType
    base_url: str
    credentials: dict[str, str]
    capabilities: list[SystemCapability] = []
    active: bool = True


class SystemConnectorResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    connector_type: ConnectorType
    base_url: str
    capabilities: list[SystemCapability]
    active: bool
    created_at: datetime
    updated_at: datetime


class RegisterCommunicationChannelDTO(BaseModel):
    name: str
    channel_type: ChannelType
    config: dict[str, str]
    capabilities: list[ChannelCapability] = []
    active: bool = True


class CommunicationChannelResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    channel_type: ChannelType
    config: dict[str, str]
    capabilities: list[ChannelCapability]
    active: bool
    created_at: datetime
    updated_at: datetime
