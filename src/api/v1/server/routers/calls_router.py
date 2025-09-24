"""Calls router."""

# -- Import

import logging
import shutil
from pathlib import Path
from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repository.database.crud import CallCRUD, get_call_crud
from src.core.repository.database.db_manager import db_manager
from src.core.config import settings
from src.core.repository.schemas import CallCreate


log = logging.getLogger(__name__)


# -- Exports

__all__ = ["calls_r"]

# --

calls_r = APIRouter(
    prefix=settings.api.v1_data_url,
    tags=["calls"],
)

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "recordings"
UPLOAD_DIR.mkdir(exist_ok=True)


@calls_r.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=UUID,
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


@calls_r.post(
    path="/{call_id}/recording/",
    status_code=status.HTTP_201_CREATED,
    name="upload-call-recording",
)
async def upload_recording(
    call_id: UUID,
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    task_crud: Annotated[CallCRUD, Depends(get_call_crud)],
    file: UploadFile = File(...),
):
    """Загружает аудиозапись звонка, сохраняет на диск и создаёт запись в БД."""

    filename = file.filename
    file_path = UPLOAD_DIR / filename

    # сохраняем файл на диск
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # создаём запись в БД
    await task_crud.create_recording(
        session=session,
        call_id=call_id,
        filename=filename,
    )
