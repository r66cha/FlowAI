"""Task schemas."""

# -- Imports

import enum
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Any


# -- Exports

__all__ = [
    "CallStatus",
    "CallCreate",
    "CallOut",
    "UploadRecordingResponse",
    "CallRead",
]

# -- Constants

CREATED = "Создано."
IN_PROGRESS = "В процессе..."
COMPLETED = "Завершен."

# -- Enums


class CallStatus(str, enum.Enum):
    created = CREATED
    in_progress = IN_PROGRESS
    completed = COMPLETED


# -- Schemas


class CallCreate(BaseModel):
    caller: str = "+79001234567"
    receiver: str = "+74951234567"
    started_at: datetime = datetime.fromisoformat("2025-09-20T10:00:00")


class CallOut(BaseModel):
    id: UUID


class UploadRecordingResponse(BaseModel):
    status: str
    task_id: Any


class RecordingRead(BaseModel):
    id: int
    duration: int
    call_id: UUID
    filename: str
    transcription: Optional[str] = None

    class Config:
        from_attributes = True


class CallRead(BaseModel):
    id: UUID
    caller: str
    receiver: str
    status: str
    started_at: datetime
    recording: Optional[RecordingRead] = None

    class Config:
        from_attributes = True
