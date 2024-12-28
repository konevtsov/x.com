from fastapi import Depends
from sqlalchemy import select, update, insert, delete, Result
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.session import connector
from schemas.user import (
    UserUpdateRequestSchema,
)
from dto.user import UserCreateDTO


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(connector.session_getter)):
        self._session = session

    async def create_user(self, user: UserCreateDTO):
        new_user = User(**user.model_dump())
        self._session.add(new_user)
        await self._session.commit()

    async def get_user_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def update_user_by_email(self, user: UserUpdateRequestSchema, email: str):
        stmt = (
            update(User).
            where(User.email == email).
            values(**user.model_dump())
        )
        await self._session.execute(stmt)
        await self._session.commit()
