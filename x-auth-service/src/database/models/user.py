from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Text

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    refresh_token: Mapped[str] = mapped_column(
        Text, unique=False, nullable=True, default="",
    )
