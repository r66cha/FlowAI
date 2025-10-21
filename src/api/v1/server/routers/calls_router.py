"""Calls router."""

# -- Import

import logging
import aiofiles

from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, UploadFile, File

from src.core.config import settings
from src.core.repository.schemas import CallCreate, UploadRecordingResponse, CallRead
from src.core.repository.tasks import process_recordings
from src.core.repository.database.crud import CallCRUD


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
async def create_call(call_in: CallCreate):
    """Записывает данные вызова и возвращает его UUID."""

    call_id = await CallCRUD.create_call(
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

    is_UUID = await CallCRUD._check_UUID(call_id)
    if not is_UUID:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UUID: %r not exist" % call_id,
        )

    filename = file.filename
    file_path = UPLOAD_DIR / (filename or "")

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
async def get_call(call_id: UUID):
    """Возвращает данные звонка по его call_id."""

    result = await CallCRUD.get_call_info(
        call_id=call_id,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data not found."
        )

    return result
