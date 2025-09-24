"""Task schemas."""

# -- Imports

import enum
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


# -- Exports

__all__ = [
    "CallStatus",
    "CallCreate",
    "CallOut",
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
