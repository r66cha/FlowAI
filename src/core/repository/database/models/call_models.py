"""Модели БД"""

# -- Imports

import uuid
import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional

from src.core.repository.schemas import CallStatus

# -- Exports

__all__ = [
    "Call",
    "Recording",
]

# --


class Base(DeclarativeBase):
    pass


class Call(Base):
    """Модель звонка"""

    __tablename__ = "calls"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,  # генерируется в Python
        nullable=False,
    )
    caller: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    receiver: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
    )
    status: Mapped[CallStatus] = mapped_column(
        Enum(CallStatus),
        default=CallStatus.created,
        nullable=False,
    )

    recording: Mapped[Optional["Recording"]] = relationship(
        back_populates="call",
        uselist=False,
    )


class Recording(Base):
    """Модель записи звонка"""

    __tablename__ = "recordings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    call_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("calls.id", ondelete="CASCADE"),
        nullable=False,
    )
    filename: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    duration: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    transcription: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    call: Mapped["Call"] = relationship(back_populates="recording")
