from fastapi import Depends
from sqlalchemy import Result, delete, func, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import Follow, User
from database.session import connector
from dto.user import UserCreateDTO
from exceptions.user_exceptions import AlreadyFollowedError
from schemas.user import (
    UserUpdateSchema,
)


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(connector.session_getter)):
        self._session = session

    async def create_user(self, user: UserCreateDTO) -> None:
        new_user = User(**user.model_dump())
        self._session.add(new_user)
        await self._session.commit()

    async def get_user_by_user_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.user_id == user_id)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def get_user_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def update_user_by_user_id(self, user: UserUpdateSchema, user_id: int) -> None:
        stmt = update(User).where(User.user_id == user_id).values(**user.model_dump())
        await self._session.execute(stmt)
        await self._session.commit()

    async def update_user_by_email(self, user: UserUpdateSchema, email: str) -> None:
        stmt = update(User).where(User.email == email).values(**user.model_dump())
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = (
            select(User)
            .options(
                selectinload(User.followers),
                selectinload(User.following),
            )
            .where(User.username == username)
        )
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def get_user_id_by_username(self, username: str) -> int | None:
        stmt = select(User.id).where(User.username == username)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def follow_by_username(self, followed_id: int, follower_id: int) -> None:
        stmt = insert(Follow).values(followed_id=followed_id, follower_id=follower_id)
        try:
            await self._session.execute(stmt)
        except IntegrityError as exc:
            raise AlreadyFollowedError from exc
        await self._session.commit()

    async def unfollow_by_username(self, followed_id: int, follower_id: int) -> None:
        stmt = delete(Follow).where(Follow.followed_id == followed_id).where(Follow.follower_id == follower_id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_user_followings(self, user_id: int):
        stmt = (
            select(User.username, User.bio)
            .outerjoin(Follow, Follow.followed_id == User.id)
            .where(Follow.follower_id == user_id)
        )
        result: Result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_user_followers(self, user_id: int):
        stmt = (
            select(User.username, User.bio)
            .outerjoin(Follow, Follow.follower_id == User.id)
            .where(Follow.followed_id == user_id)
        )
        result: Result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_username_exist_count(self, username: str):
        stmt = select(func.count()).select_from(User).where(User.username == username)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def add_avatar_url_by_user_id(self, user_id: int, avatar_url: str):
        stmt = update(User).where(User.user_id == user_id).values(avatar_url=avatar_url)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_avatar_url_by_user_id(self, user_id: int):
        stmt = update(User).values(avatar_url="").where(User.user_id == user_id)
        # stmt = delete(User.avatar_url).where(User.user_id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()
