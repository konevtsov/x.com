from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Follow(Base):
    followed_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    follower_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    followed_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[followed_id],
        back_populates="followers",
    )
    follower_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following",
    )

    __table_args__ = (UniqueConstraint("followed_id", "follower_id", name="unique_follow"),)
