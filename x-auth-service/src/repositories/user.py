from fastapi import Depends
from sqlalchemy import Result, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.session import connector
from schemas.auth import JWTTokenUpdateSchema
from schemas.user import UserCreateSchema


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(connector.session_getter)):
        self._session = session

    async def email_exists(self, email: str) -> bool:
        stmt = select(User).where(User.email == email)
        result: Result = await self._session.execute(stmt)
        return bool(result.scalar())

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def create_user(self, user: UserCreateSchema) -> int:
        stmt = insert(User).values(**user.model_dump()).returning(User.id)
        result: Result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar()

    async def update_refresh_token_by_email(self, data: JWTTokenUpdateSchema) -> None:
        stmt = update(User).where(User.email == data.email).values(refresh_token=data.refresh_token)
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_token_by_email(self, email: str) -> str:
        stmt = select(User.refresh_token).where(User.email == email)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def delete_token_by_email(self, email: str):
        stmt = update(User).where(User.email == email).values(refresh_token="")
        await self._session.execute(stmt)
        await self._session.commit()
