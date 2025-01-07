from fastapi import Depends
from sqlalchemy import select, update, insert, delete, Result, text
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Follow
from database.session import connector
from schemas.user import (
    UserUpdateRequestSchema, FollowSchema,
)
from dto.user import UserCreateDTO
from exceptions.user_exceptions import UserNotFoundError


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

    async def get_user_by_username(self, username: str):
        stmt = select(User).where(User.username == username)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def get_user_id_by_username(self, username: str):
        stmt = select(User.id).where(User.username == username)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def follow_by_username(self, followed_id: int, follower_id: int):
        stmt = insert(Follow).values(user_id=followed_id, follower_id=follower_id)
        await self._session.execute(stmt)
        await self._session.commit()
