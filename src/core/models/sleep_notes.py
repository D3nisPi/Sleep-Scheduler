from __future__ import annotations

from datetime import time, date
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base
if TYPE_CHECKING:
    from src.core.models.users import UsersORM


class SleepNotesORM(Base):
    __tablename__ = "sleep_notes"
    __table_args__ = (UniqueConstraint("user_id", "note_date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    note_date: Mapped[date]
    sleep_start: Mapped[time]
    sleep_end: Mapped[time]
    rating: Mapped[int | None] = mapped_column(CheckConstraint("rating IS NULL OR (rating >= 1 AND rating <= 5)"))
    comment: Mapped[str | None] = mapped_column(String(300))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))

    # FIXME
    # Removed due to circular import error
    # user: Mapped["UsersORM"] = relationship("UsersORM", back_populates="sleep_notes")
