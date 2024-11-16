from datetime import time, date
from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base
if TYPE_CHECKING:
    from src.core.models.users import UsersOrm


class SleepNotesOrm(Base):
    __tablename__ = "sleep_notes"
    __table_args__ = (UniqueConstraint("user_id", "note_date"))

    id: Mapped[int] = mapped_column(primary_key=True)
    note_date: Mapped[date]
    sleep_start: Mapped[time]
    sleep_end: Mapped[time]
    rating: Mapped[int | None] = mapped_column(check="rating IS NULL OR (rating >= 1 AND rating <= 5)")
    comment: Mapped[str | None] = mapped_column(String(300))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))

    user: Mapped["UsersOrm"] = relationship(back_populates="sleep_notes")
