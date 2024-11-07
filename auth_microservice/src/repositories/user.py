from fastapi import Depends
from sqlalchemy import Result, select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from schemas.user import UserSchema
from schemas.auth import JWTToken
from database.session import connector


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(connector.session_getter)):
        self._session = session

    async def username_exists(self, username: str) -> bool:
        stmt = select(User).where(User.username == username)
        result: Result = await self._session.execute(stmt)
        return bool(result.scalar())

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def create_user(self, user: UserSchema) -> None:
        new_user = User(**user.model_dump())
        self._session.add(new_user)
        await self._session.commit()

    async def update_refresh_token_by_username(self, data: JWTToken) -> None:
        stmt = (
            update(User).
            where(User.username == data.username).
            values(refresh_token=data.refresh_token)
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_token_by_username(self, username: str) -> str:
        stmt = (
            select(User.refresh_token).
            where(User.username == username)
        )
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def delete_token(self, username: str):
        stmt = (
            update(User).
            where(User.username == username).
            values(refresh_token="")
        )
        await self._session.execute(stmt)
        await self._session.commit()
