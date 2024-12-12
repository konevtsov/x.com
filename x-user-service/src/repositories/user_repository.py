from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.session import connector
from schemas.user import (
    UserUpdateScheme,
    UserInScheme,
)


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(connector.session_getter)):
        self._session = session

    async def create_user(self, user: UserInScheme):
        new_user = User(**user.model_dump())
        self._session.add(new_user)
        await self._session.commit()

    async def update_user(self, user: UserUpdateScheme):
        stmt = (
            update(User).
            where(User.username == user.username).
            values(**user.model_dump())
        )
        await self._session.execute(stmt)
        await self._session.commit()
