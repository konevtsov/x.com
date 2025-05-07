from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .post import Post


class Like(Base):
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="likes")

    __table_args__ = (UniqueConstraint("post_id", "user_id", name="unique_like"),)
