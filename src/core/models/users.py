from __future__ import annotations


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    display_name: Mapped[str] = mapped_column(String(50))
    password_hash: Mapped[str] = mapped_column(String(120))
    refresh_token_id: Mapped[str | None] = mapped_column(String(32))
