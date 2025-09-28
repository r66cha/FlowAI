"""Recording task."""

# -- Imports

import asyncio
import logging


from pydub import AudioSegment
from src.core.repository.services.celery import celery_app
from typing import TYPE_CHECKING

from src.core.repository.database.crud import CallCRUD
from src.core.repository.database.db_manager import db_manager

from uuid import UUID


if TYPE_CHECKING:
    pass


# -- Exports

__all__ = ["process_recordings"]

# --

log = logging.getLogger(__name__)


@celery_app.task
def process_recordings(
    file_path: str,
    call_id: str,
    filename: str,
):

    audio = AudioSegment.from_file(file_path)
    duration_sec = len(audio) / 1000

    first_20_sec = audio[: 20 * 1000]

    log.info("Detected speech fragment:: %s", first_20_sec)  # Псевдотранскрипция

    async def _save():
        async for session in db_manager.get_session():
            crud = CallCRUD()
            await crud.create_recording(
                session=session,
                call_id=UUID(call_id),
                filename=filename,
                duration=duration_sec,
                transcription=str(first_20_sec),
            )

    asyncio.run(_save())
