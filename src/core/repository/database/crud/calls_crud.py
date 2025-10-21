"""CRUD"""

# --- Imports

import logging
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from src.core.repository.database.models import Call, Recording  # noqa: F401
from uuid import UUID
from src.core.repository.database.db_manager import db_manager
from typing import Callable, Optional
from collections.abc import AsyncGenerator, Generator


# -- Exports

__all__ = [
    "CallCRUD",
]

# --

log = logging.getLogger(__name__)


# --


class CallCRUD:

    async_session_factory: Optional[
        Callable[[], AsyncGenerator[AsyncSession, None]]
    ] = None
    sync_session_factory: Optional[Callable[[], Generator[Session, None]]] = None

    @classmethod
    def set_session_factory(
        cls,
        async_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
        sync_factory: Callable[[], Generator[Session, None]],
    ):
        cls.async_session_factory = async_factory  # type: ignore
        cls.sync_session_factory = sync_factory  # type: ignore

    @classmethod
    async def _check_async_session(cls) -> None:
        if cls.async_session_factory is None:  # type: ignore
            raise RuntimeError("Session factory not set")

    @classmethod
    def _check_sync_session(cls) -> None:
        if cls.sync_session_factory is None:  # type: ignore
            raise RuntimeError("Session factory not set")

    @classmethod
    async def _get_async_session(cls) -> AsyncGenerator[AsyncSession, None]:
        await cls._check_async_session()
        async for session in cls.async_session_factory():  # type: ignore
            yield session

    @classmethod
    def _get_sync_session(cls) -> Generator[Session, None]:
        cls._check_sync_session()
        for session in cls.sync_session_factory():  # type: ignore
            yield session

    @classmethod
    async def create_call(
        cls,
        caller: str,
        receiver: str,
    ) -> UUID:
        """Создаёт запись данных о звонке."""

        call = Call(caller=caller, receiver=receiver)
        async for session in cls._get_async_session():
            session.add(call)
            await session.commit()
            await session.refresh(call)

        return call.id

    @classmethod
    def create_recording(
        cls,
        call_id: UUID,
        filename: str,
        duration: int,
        transcription: str,
    ) -> dict | None:
        """Создаёт запись о прикреплённой аудиозаписи звонка."""

        recording = Recording(
            call_id=call_id,
            filename=filename,
            duration=duration,
            transcription=transcription,
        )
        for session in cls._get_sync_session():
            session.add(recording)
            session.commit()

    @classmethod
    async def get_call_info(
        cls,
        call_id: UUID,
    ):
        """Возвращает информацию о звонке."""

        stmt = (
            select(Call).where(Call.id == call_id).options(selectinload(Call.recording))
        )
        async for session in cls._get_async_session():
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def _check_UUID(cls, call_id: UUID) -> bool:
        stmt = select(Call).where(Call.id == call_id)
        async for session in cls._get_async_session():
            result = await session.execute(stmt)
            call = result.scalar_one_or_none()
            return call is not None
        return False


CallCRUD.set_session_factory(db_manager.get_session, db_manager.get_sync_session)
