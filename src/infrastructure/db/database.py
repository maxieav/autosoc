from __future__ import annotations
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.infrastructure.config import get_settings


class Base(DeclarativeBase):
    pass


def create_engine_and_session(database_url: str | None = None):
    settings = get_settings()
    url = database_url or settings.database_url
    engine = create_async_engine(url, echo=settings.debug)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return engine, session_factory


engine, AsyncSessionLocal = create_engine_and_session()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
