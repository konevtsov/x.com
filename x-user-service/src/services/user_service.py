from fastapi import Depends

from schemas.user import (
    FullUserSchema,
    PartialUserSchema,
    FollowSchema,
    UnfollowSchema,
    UserUpdateSchema,
    AvatarUploadSchema,
    DeleteAvatarSchema,
    GetAvatarSchema,
)
from repositories.user_repository import UserRepository
from schemas.token import TokenIntrospectSchema
from exceptions.user_exceptions import (
    UserNotFoundError,
    FollowYourselfError,
    UnfollowYourselfError,
    UsernameAlreadyExistsError,
    AvatarNotFoundError,
)
from dto.user import UserCreateDTO
from services.s3_service import s3_service


AVATARS_FOLDER_NAME = "profile_images"
ORIGINAL_AVATAR_FILENAME = "original"


class UserService:
    def __init__(
        self,
        repository: UserRepository = Depends(UserRepository),
    ):
        self._repository = repository

    async def create_user(self, user: UserCreateDTO):
        await self._repository.create_user(user=user)

    async def update_user(self, user_update: UserUpdateSchema, user_token: TokenIntrospectSchema):
        user = await self._repository.get_user_by_user_id(user_id=user_token.user_id)
        if not user:
            raise UserNotFoundError
        if await self._repository.get_username_exist_count(username=user_update.username) > 1:
            raise UsernameAlreadyExistsError
        await self._repository.update_user_by_user_id(user_update, user_id=user_token.user_id)

    async def get_user_by_username(self, username: str, user_token: TokenIntrospectSchema):
        user = await self._repository.get_user_by_username(username=username)
        if not user:
            raise UserNotFoundError
        if user_token.user_id == user.user_id:
            return FullUserSchema.model_validate(user)

        return PartialUserSchema.model_validate(user)

    async def get_followings_by_username(self, username: str):
        user = await self._repository.get_user_by_username(username=username)
        if not user:
            raise UserNotFoundError
        return await self._repository.get_user_followings(user_id=user.id)

    async def get_followers_by_username(self, username: str):
        user = await self._repository.get_user_by_username(username=username)
        if not user:
            raise UserNotFoundError
        return await self._repository.get_user_followers(user_id=user.id)

    async def follow(self, follow_schema: FollowSchema):
        followed_id = await self._repository.get_user_id_by_username(follow_schema.followed_username)
        if follow_schema.follower_id == followed_id:
            raise FollowYourselfError
        if not follow_schema.follower_id or not followed_id:
            raise UserNotFoundError
        await self._repository.follow_by_username(followed_id, follow_schema.follower_id)

    async def unfollow(self, unfollow_schema: UnfollowSchema):
        followed_id = await self._repository.get_user_id_by_username(unfollow_schema.followed_username)
        if followed_id == unfollow_schema.follower_id:
            raise UnfollowYourselfError
        if not unfollow_schema.follower_id or not followed_id:
            raise UserNotFoundError
        await self._repository.unfollow_by_username(followed_id, unfollow_schema.follower_id)

    async def upload_avatar(self, upload_schema: AvatarUploadSchema, user_token: TokenIntrospectSchema):
        key = str(user_token.user_id)
        destination_path = f"{AVATARS_FOLDER_NAME}/{key}/{ORIGINAL_AVATAR_FILENAME}.{upload_schema.file_extension}"
        await self._repository.add_avatar_url_by_user_id(user_id=user_token.user_id, avatar_url=destination_path)

        await s3_service.upload_file(
            destination_path=destination_path,
            content=upload_schema.content,
        )

    async def get_avatar_by_username(self, get_avatar_schema: GetAvatarSchema):
        user = await self._repository.get_user_by_username(username=get_avatar_schema.username)
        if not user.avatar_url:
            raise AvatarNotFoundError
        data = await s3_service.get_file(key=user.avatar_url)

        return data

    async def delete_avatar(self, remove_schema: DeleteAvatarSchema):
        user = await self._repository.get_user_by_user_id(user_id=remove_schema.user_id)
        if not user.avatar_url:
            raise AvatarNotFoundError
        await s3_service.delete_file(key=user.avatar_url)
        await self._repository.delete_avatar_url_by_user_id(user_id=remove_schema.user_id)
