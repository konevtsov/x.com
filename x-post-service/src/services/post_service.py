from fastapi import Depends

from database.models import Post
from exceptions.base_exception import PermissionDeniedError
from exceptions.post_exceptions import PostNotFoundError
from repositories.post_repository import PostRepository
from schemas.post import PostCreateSchema, PostDeleteSchema, PostSchema


class PostService:
    def __init__(
        self,
        post_repository: PostRepository = Depends(PostRepository),
    ):
        self._post_repository = post_repository

    async def create_post(self, post_create: PostCreateSchema):
        await self._post_repository.create_post(post_create)

    async def delete_post(self, post_delete: PostDeleteSchema):
        post: Post | None = await self._post_repository.get_post_by_id(post_id=post_delete.post_id)
        if not post:
            raise PostNotFoundError
        if post.user_id != post_delete.user_id:
            raise PermissionDeniedError
        await self._post_repository.delete_post_by_id(post_id=post_delete.post_id)

    async def get_all_posts_by_username(self, username: str):
        posts: list[Post] = await self._post_repository.get_all_posts_by_username(username=username)
        if not posts:
            raise PostNotFoundError

        validate_posts = []
        for i in range(len(posts)):
            validate_posts.append(PostSchema.model_validate(posts[i]).dict())
        return validate_posts

    async def get_post_by_id(self, post_id: int):
        post: Post | None = await self._post_repository.get_post_by_id(post_id=post_id)
        if not post:
            raise PostNotFoundError

        return PostSchema.model_validate(post)
