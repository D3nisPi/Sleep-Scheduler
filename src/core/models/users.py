from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base

if TYPE_CHECKING:
    from src.core.models.sleep_goals import SleepGoalsORM
    from src.core.models.sleep_notes import SleepNotesORM


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    display_name: Mapped[str] = mapped_column(String(50))
    password_hash: Mapped[str] = mapped_column(String(120))
    refresh_token_id: Mapped[str | None] = mapped_column(String(32))

    # FIXME
    # Removed due to circular import error
    # sleep_goal: Mapped["SleepGoalsORM"] = relationship(
    #     "SleepGoalsORM",
    #     back_populates="user",
    #     cascade="all, delete",
    #     passive_deletes=True
    # )
    # sleep_notes: Mapped[list["SleepNotesORM"]] = relationship("SleepNotesORM",
    #                                                           back_populates="user",
    #                                                           cascade="all, delete")
