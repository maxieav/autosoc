from __future__ import annotations
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CreateTenantDTO(BaseModel):
    name: str
    active: bool = True
    system_connectors: list[dict] = []
    communication_channels: list[dict] = []


class UpdateTenantDTO(BaseModel):
    name: str | None = None
    active: bool | None = None
    system_connectors: list[dict] | None = None
    communication_channels: list[dict] | None = None


class TenantResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    active: bool
    system_connectors: list[dict]
    communication_channels: list[dict]
    created_at: datetime
    updated_at: datetime
