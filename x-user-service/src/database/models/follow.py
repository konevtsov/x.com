from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, String, Integer, ForeignKey, UniqueConstraint

from .base import Base


if TYPE_CHECKING:
    from .user import User


class Follow(Base):
    followed_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    follower_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    followed_user: Mapped["User"] = relationship(
        "User", foreign_keys=[followed_id], back_populates="followers", cascade="all, delete-orphan",
    )
    follower_user: Mapped["User"] = relationship(
        "User", foreign_keys=[follower_id], back_populates="following", cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("followed_id", "follower_id", name="unique_follow"),
    )
