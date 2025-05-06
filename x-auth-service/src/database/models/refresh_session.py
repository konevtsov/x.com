from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class RefreshSession(Base):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    refresh_token_uuid: Mapped[str] = mapped_column(Uuid(as_uuid=False), default="")
    refresh_token: Mapped[str] = mapped_column(Text, default="")
    ip: Mapped[str] = mapped_column(String(16))

    user: Mapped["User"] = relationship("User", back_populates="refresh_sessions")
