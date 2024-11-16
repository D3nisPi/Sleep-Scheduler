from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base
if TYPE_CHECKING:
    from src.core.models.users import UsersORM


class SleepGoalsORM(Base):
    __tablename__ = "sleep_goals"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",
                                                    ondelete="CASCADE",
                                                    onupdate="CASCADE"),
                                         primary_key=True)
    sleep_start: Mapped[time]
    sleep_end: Mapped[time]

    # FIXME
    # Removed due to circular import error
    # user: Mapped["UsersORM"] = relationship("UsersORM", back_populates="sleep_goal")
