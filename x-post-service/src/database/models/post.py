from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .like import Like


class Post(Base):
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    author_username: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String(280))

    likes: Mapped[list["Like"]] = relationship("Like", back_populates="post")

    @property
    def likes_count(self) -> int:
        return len(self.likes)
