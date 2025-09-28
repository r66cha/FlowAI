"""DB Manager."""

# -- Imports

import logging
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from collections.abc import AsyncGenerator, Generator
from .db_config import db_url

# -- Exports

__all__ = ["db_manager", "DatabaseManager"]

# --

log = logging.getLogger(__name__)

# --

# по SOLID нужно создать 2 отдельных класса для sync и async Managers


class DatabaseManager:
    def __init__(self, db_url: str):
        self.async_engine: AsyncEngine = create_async_engine(db_url)
        self.async_session_factory: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self.async_engine,
                expire_on_commit=False,
            )
        )

        sync_db_url = db_url.replace("+asyncpg", "")
        self.engine = create_engine(sync_db_url)
        self.session_factory: sessionmaker[Session] = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.async_engine.dispose()
        self.engine.dispose()
        log.info("The database core has been deleted")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_factory() as session:
            yield session

    def get_sync_session(self) -> Generator[Session, None]:
        with self.session_factory() as session:
            yield session


db_manager = DatabaseManager(db_url=db_url.get_DB_URL_API)
