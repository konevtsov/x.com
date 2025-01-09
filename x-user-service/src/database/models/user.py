from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, String

from .base import Base
from .follow import Follow


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    bio: Mapped[str] = mapped_column(String(160), nullable=True)
    website: Mapped[str] = mapped_column(String(100), nullable=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)

    followers: Mapped[list["Follow"]] = relationship("Follow", foreign_keys="Follow.followed_id", back_populates="followed_user")
    following: Mapped[list["Follow"]] = relationship("Follow", foreign_keys="Follow.follower_id", back_populates="follower_user")

    @property
    def followers_count(self):
        return len(self.followers)

    @property
    def followings_count(self):
        return len(self.following)
