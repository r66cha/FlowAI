"""Task router."""

# -- Import

import logging
from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.repository.database.crud import CallCRUD, get_call_crud
from src.core.repository.database import db_manager
from src.core.config import settings

from src.core.repository.schemas import CallCreate, CallOut


log = logging.getLogger(__name__)


# -- Exports

__all__ = ["calls_r"]

# --

calls_r = APIRouter(
    prefix=settings.api.v1_data_url,
    tags=["calls"],
)


@calls_r.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=CallOut,
    name="crete-call",
)
async def create_call(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[CallCRUD, Depends(get_call_crud)],
    call_in: CallCreate,
):
    """Записывает данные вызова и возвращает его UUID."""

    call_id = await task_crud.create_call(
        session=session,
        caller=call_in.caller,
        receiver=call_in.receiver,
    )

    return call_id
