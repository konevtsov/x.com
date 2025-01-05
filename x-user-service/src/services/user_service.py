from fastapi import Depends

from schemas.user import (
    FullUserSchema,
    PartialUserSchema,
    UserUpdateRequestSchema,
)
from repositories.user_repository import UserRepository
from schemas.token import TokenIntrospectSchema
from exceptions.user_exceptions import (
    UserNotFoundError,
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
