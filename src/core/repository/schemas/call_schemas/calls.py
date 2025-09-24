"""Task schemas."""

# -- Imports

import enum
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
    caller: str
    receiver: str


class CallOut(BaseModel):
    id: UUID
