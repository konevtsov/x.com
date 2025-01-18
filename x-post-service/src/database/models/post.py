from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Text

from .base import Base


class Post(Base):
    author_username: Mapped[str] = mapped_column(String(32), unique=False)
    author_email: Mapped[str] = mapped_column(Text, unique=False)
    text: Mapped[str] = mapped_column(String(280))
