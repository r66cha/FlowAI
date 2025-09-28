"""CRUD"""

# --- Imports

import logging
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.repository.database.models import Call, Recording  # noqa: F401
from uuid import UUID


# -- Exports

__all__ = [
    "get_call_crud",
    "CallCRUD",
]

# --

log = logging.getLogger(__name__)


# --


class CallCRUD:

    async def create_call(
        self,
        session: AsyncSession,
        caller: str,
        receiver: str,
    ) -> UUID:
        """Создаёт запись данных о звонке."""

        call = Call(caller=caller, receiver=receiver)
        session.add(call)
        await session.commit()
        await session.refresh(call)

        return call.id

    def create_recording(
        self,
        session: AsyncSession,
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
        session.add(recording)
        session.commit()

    async def get_call_info(
        self,
        session: AsyncSession,
        call_id: UUID,
    ):
        """Возвращает информацию о звонке."""

        stmt = (
            select(Call).where(Call.id == call_id).options(selectinload(Call.recording))
        )
        result = await session.execute(stmt)

        return result.scalar_one_or_none()


async def get_call_crud():
    return CallCRUD()
