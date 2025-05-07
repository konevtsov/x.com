from fastapi import Depends
from sqlalchemy import Result, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models import Post
from database.session import connector
from schemas.post import PostCreateSchema


class PostRepository:
    def __init__(
        self,
        session: AsyncSession = Depends(connector.session_getter),
    ):
        self._session = session

    async def create_post(self, post_create: PostCreateSchema):
        post = Post(**post_create.model_dump())
        self._session.add(post)
        await self._session.commit()

    async def get_post_by_id(self, post_id: int):
        stmt = select(Post).options(selectinload(Post.likes)).where(Post.id == post_id)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def delete_post_by_id(self, post_id: int):
        stmt = delete(Post).where(Post.id == post_id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_all_posts_by_username(self, username: str):
        stmt = select(Post).options(selectinload(Post.likes)).where(Post.author_username == username)
        result: Result = await self._session.execute(stmt)
        return result.scalars().all()
