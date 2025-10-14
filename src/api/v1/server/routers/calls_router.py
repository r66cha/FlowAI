"""Calls router."""

# -- Import

import logging
import aiofiles

from pathlib import Path
from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repository.database.crud import CallCRUD, get_call_crud
from src.core.repository.database.db_manager import db_manager
from src.core.config import settings
from src.core.repository.schemas import CallCreate, UploadRecordingResponse, CallRead
from src.core.repository.tasks import process_recordings


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
    call_crud: Annotated[CallCRUD, Depends(get_call_crud)],
    call_in: CallCreate,
):
    """Записывает данные вызова и возвращает его UUID."""

    call_id = await call_crud.create_call(
        session=session,
        caller=call_in.caller,
        receiver=call_in.receiver,
    )

    return call_id


@calls_r.post(
    path="/{call_id}/recording/",
    status_code=status.HTTP_201_CREATED,
    response_model=UploadRecordingResponse,
    name="upload-call-recording",
)
async def upload_recording(
    call_id: UUID,
    file: UploadFile = File(...),
):
    """Загружает аудиозапись звонка, сохраняет на диск и создаёт запись в БД."""

    filename = file.filename
    file_path = UPLOAD_DIR / filename

    async with aiofiles.open(file_path, "wb") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)

    task = process_recordings.delay(
        file_path=str(file_path),
        call_id=str(call_id),
        filename=filename,
    )

    return {"status": f"{filename} saved", "task_id": task.id}


@calls_r.get(
    path="/{call_id}",
    status_code=status.HTTP_200_OK,
    response_model=CallRead,
    name="call-info-get",
)
async def get_call(
    session: Annotated[AsyncSession, Depends(db_manager.get_session)],
    call_crud: Annotated[CallCRUD, Depends(get_call_crud)],
    call_id: UUID,
):
    """Возвращает данные звонка по его call_id."""

    result = await call_crud.get_call_info(
        session=session,
        call_id=call_id,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data not found."
        )

    return result
