from fastapi import Depends

from .password_service import PasswordService
from .jwt_service import JWTService
from .token_service import TokenService
from repositories.user import UserRepository
from schemas.auth import (
    SignUpRequest,
    SignInRequest,
    CredentialsResponse,
)
from schemas.user import UserSchema
from excepltions.auth import (
    UserAlreadyExistsException,
)


class AuthService:
    def __init__(
        self,
        password_service: PasswordService = Depends(PasswordService),
        repository: UserRepository = Depends(UserRepository),
        token_service: TokenService = Depends(TokenService),
    ):
        self.repository = repository
        self._password_service = password_service
        self._token_service = token_service

    async def sign_up(self, request: SignUpRequest) -> CredentialsResponse:
        if await self.repository.username_exists(request.username):
            raise UserAlreadyExistsException

        password_hash = self._password_service.hash_password(request.password)

        new_user = UserSchema(
            username=request.username,
            password=str(password_hash),
        )
        await self.repository.create_user(new_user)
        refresh_token = self._token_service.create_refresh_token(new_user)
        access_token = self._token_service.create_access_token(new_user)
        await self.repository.update_refresh_token_by_username(
            username=new_user.username,
            refresh_token=refresh_token,
        )

        return CredentialsResponse(access_token=access_token, refresh_token=refresh_token)
