from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from fastapi import FastAPI
from src.infrastructure.db.database import engine, Base
from src.presentation.api.routers import cases, tenants, connectors, channels, webhooks, health


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="AutoSOC", version="0.1.0", lifespan=lifespan)
app.include_router(health.router, tags=["health"])
app.include_router(cases.router, prefix="/api/v1/cases", tags=["cases"])
app.include_router(tenants.router, prefix="/api/v1/tenants", tags=["tenants"])
app.include_router(connectors.router, prefix="/api/v1/connectors", tags=["connectors"])
app.include_router(channels.router, prefix="/api/v1/channels", tags=["channels"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["webhooks"])
