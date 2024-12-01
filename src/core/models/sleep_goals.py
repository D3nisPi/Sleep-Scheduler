from __future__ import annotations

from datetime import time

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base


class SleepGoalsORM(Base):
    __tablename__ = "sleep_goals"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    sleep_start: Mapped[time]
    sleep_end: Mapped[time]
