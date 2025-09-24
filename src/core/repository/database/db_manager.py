"""Менеджер БД."""

# -- Imports

import logging
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from collections.abc import AsyncGenerator
from .db_config import db_url

# -- Exports

__all__ = ["db_manager"]

# --

log = logging.getLogger(__name__)

# --


class DatabaseManager:
    def __init__(self, db_url):
        self.engine: AsyncEngine = create_async_engine(db_url)
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()
        log.info("Ядро базы данных удалено")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_manager = DatabaseManager(db_url=db_url.get_DB_URL_API)
