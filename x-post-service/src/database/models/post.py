from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Text

from .base import Base


class Post(Base):
    author_id: Mapped[int]
    author_username: Mapped[str] = mapped_column(String(32), unique=True)
    content: Mapped[str] = mapped_column(String(280))
