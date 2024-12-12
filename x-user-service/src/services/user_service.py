from fastapi import Depends

from schemas.user import (
    UserUpdateScheme,
    UserInScheme,
)
from repositories.user_repository import UserRepository


class UserService:
    def __init__(
        self,
        repository: UserRepository = Depends(UserRepository),
    ):
        self._repository = repository

    async def create_user(self, user: UserInScheme):
        await self._repository.create_user(user=user)

    async def update_user(self, user: UserUpdateScheme):
        await self._repository.update_user(user)
