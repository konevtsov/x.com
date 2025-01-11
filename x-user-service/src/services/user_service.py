from fastapi import Depends

from schemas.user import (
    FullUserSchema,
    PartialUserSchema,
    UserUpdateRequestSchema,
    FollowSchema,
    UnfollowSchema,
)
from repositories.user_repository import UserRepository
from schemas.token import TokenIntrospectSchema
from exceptions.user_exceptions import (
    UserNotFoundError,
    FollowYourselfError,
    UnfollowYourselfError,
)
from dto.user import UserCreateDTO


class UserService:
    def __init__(
        self,
        repository: UserRepository = Depends(UserRepository),
    ):
        self._repository = repository

    async def create_user(self, user: UserCreateDTO):
        await self._repository.create_user(user=user)

    async def update_user(self, user_update: UserUpdateRequestSchema, user_token: TokenIntrospectSchema):
        user = await self._repository.get_user_by_email(email=user_token.email)
        if not user:
            raise UserNotFoundError
        await self._repository.update_user_by_email(user_update, email=user_token.email)

    async def get_user_by_username(self, username: str, user_token: TokenIntrospectSchema):
        user = await self._repository.get_user_by_username(username=username)
        if not user:
            raise UserNotFoundError
        if user_token.email == user.email:
            return FullUserSchema.model_validate(user)

        return PartialUserSchema.model_validate(user)


    async def get_followers_by_username(self, username: str):
        user = await self._repository.get_user_by_username(username=username)
        if not user:
            raise UserNotFoundError
        return await self._repository.get_user_followers(user_id=user.id)

    async def follow(self, follow_schema: FollowSchema):
        if follow_schema.followed_username == follow_schema.follower_username:
            raise FollowYourselfError
        followed_id = await self._repository.get_user_id_by_username(follow_schema.followed_username)
        follower_id = await self._repository.get_user_id_by_username(follow_schema.follower_username)
        if not follower_id or not followed_id:
            raise UserNotFoundError
        await self._repository.follow_by_username(followed_id, follower_id)

    async def unfollow(self, unfollow_schema: UnfollowSchema):
        if unfollow_schema.followed_username == unfollow_schema.follower_username:
            raise UnfollowYourselfError
        followed_id = await self._repository.get_user_id_by_username(unfollow_schema.followed_username)
        follower_id = await self._repository.get_user_id_by_username(unfollow_schema.follower_username)
        if not follower_id or not followed_id:
            raise UserNotFoundError
        await self._repository.unfollow_by_username(followed_id, follower_id)
