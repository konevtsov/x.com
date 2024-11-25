from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, Text, String

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    bio: Mapped[str] = mapped_column(String(160))
    website: Mapped[str] = mapped_column(String(100), nullable=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
