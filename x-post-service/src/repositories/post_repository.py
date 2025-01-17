from fastapi import Depends
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
