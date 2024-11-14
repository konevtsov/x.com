from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Text

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    about_me: Mapped[str] = mapped_column(String)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
