from __future__ import annotations
from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/{connector_id}")
async def handle_webhook(connector_id: str, request: Request) -> dict[str, str]:
    await request.json()
    return {"status": "received", "connector_id": connector_id}
