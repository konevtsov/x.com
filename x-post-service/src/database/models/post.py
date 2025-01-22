from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Text

from .base import Base


if TYPE_CHECKING:
    from .like import Like


class Post(Base):
    author_username: Mapped[str] = mapped_column(String(32), unique=False)
    author_email: Mapped[str] = mapped_column(Text, unique=False)
    text: Mapped[str] = mapped_column(String(280))

    likes: Mapped[list["Like"]] = relationship("Like", back_populates="post")

    @property
    def likes_count(self) -> int:
        return len(self.likes)
