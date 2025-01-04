from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Text

from .base import Base

if TYPE_CHECKING:
    from .refresh_session import RefreshSession


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    refresh_sessions: Mapped[list["RefreshSession"]] = relationship("RefreshSession", back_populates="user", cascade="all, delete-orphan")
