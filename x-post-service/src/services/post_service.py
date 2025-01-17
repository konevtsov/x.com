from fastapi import Depends

from repositories.post_repository import PostRepository
from schemas.post import PostCreateSchema


class PostService:
    def __init__(
        self,
        post_repository: PostRepository = Depends(PostRepository),
    ):
        self._post_repository = post_repository

    async def create_post(self, post_create: PostCreateSchema):
        await self._post_repository.create_post(post_create)
