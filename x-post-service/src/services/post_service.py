from fastapi import Depends

from repositories.post_repository import PostRepository
from schemas.post import PostCreateSchema, PostDeleteSchema
from exceptions.base_exception import PermissionDeniedError
from exceptions.post_exceptions import PostNotFoundError


class PostService:
    def __init__(
        self,
        post_repository: PostRepository = Depends(PostRepository),
    ):
        self._post_repository = post_repository

    async def create_post(self, post_create: PostCreateSchema):
        await self._post_repository.create_post(post_create)

    async def delete_post(self, post_delete: PostDeleteSchema):
        post = await self._post_repository.get_post_by_id(post_id=post_delete.post_id)
        if not post:
            raise PostNotFoundError
        if post.author_email != post_delete.author_email:
            raise PermissionDeniedError
        await self._post_repository.delete_post_by_id(post_id=post_delete.post_id)
