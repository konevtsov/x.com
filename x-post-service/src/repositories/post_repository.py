from fastapi import Depends
from sqlalchemy import select, insert, delete, update, Result
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import connector
from database.models import Post
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
        stmt = select(Post).where(Post.id == post_id)
        result: Result = await self._session.execute(stmt)
        return result.scalar()

    async def delete_post_by_id(self, post_id: int):
        stmt = delete(Post).where(Post.id == post_id)
        await self._session.execute(stmt)
        await self._session.commit()
