"""CRUD"""

# --- Imports

import logging
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

        call = Call(caller=caller, receiver=receiver)
        session.add(call)
        await session.commit()
        await session.refresh(call)

        return call.id


async def get_call_crud():
    return CallCRUD()
