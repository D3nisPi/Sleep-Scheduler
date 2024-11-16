from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base

if TYPE_CHECKING:
    from src.core.models.sleep_goals import SleepGoalsOrm
    from src.core.models.sleep_notes import SleepNotesOrm


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    display_name: Mapped[str] = mapped_column(String(50))
    password_hash: Mapped[str] = mapped_column(String(120))
    refresh_token_id: Mapped[str | None] = mapped_column(String(32))

    sleep_goal: Mapped["SleepGoalsOrm"] = relationship(
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True
    )
    sleep_notes: Mapped[list["SleepNotesOrm"]] = relationship(back_populates="user", cascade="all, delete")
