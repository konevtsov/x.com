from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Text, Integer, ForeignKey, UniqueConstraint

from .base import Base


if TYPE_CHECKING:
    from .post import Post


class Like(Base):
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))
    author_email: Mapped[str] = mapped_column(Text)

    post: Mapped["Post"] = relationship("Post", back_populates="likes")

    __table_args__ = (
        UniqueConstraint("post_id", "author_email", name="unique_like"),
    )
