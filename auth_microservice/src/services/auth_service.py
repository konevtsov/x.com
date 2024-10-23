from fastapi import Depends

from .password_service import PasswordService
from .jwt_service import JWTService
from .token_service import TokenService
from repositories.user import UserRepository
from schemas.auth import (
    SignUpRequest,
    SignInRequest,
    CredentialsResponse,
    JWTToken,
    TokenData,
)
from schemas.user import UserSchema
from excepltions.auth import (
    UserAlreadyExistsException,
    UserNotFoundException,
    WrongPasswordException,
)


class AuthService:
    def __init__(
        self,
        password_service: PasswordService = Depends(PasswordService),
        repository: UserRepository = Depends(UserRepository),
        token_service: TokenService = Depends(TokenService),
    ):
        self._repository = repository
        self._password_service = password_service
        self._token_service = token_service

    async def sign_up(self, request: SignUpRequest) -> CredentialsResponse:
        if await self._repository.username_exists(request.username):
            raise UserAlreadyExistsException

        password_hash = self._password_service.hash_password(request.password)
        token_data = TokenData(username=request.username)
        refresh_token = self._token_service.create_refresh_token(token_data)
        access_token = self._token_service.create_access_token(token_data)

        new_user = UserSchema(
            username=request.username,
            password=str(password_hash),
            refresh_token=refresh_token,
        )
        await self._repository.create_user(new_user)

        return CredentialsResponse(access_token=access_token, refresh_token=refresh_token)

    async def sign_in(self, request: SignInRequest) -> CredentialsResponse:
        user = await self._repository.get_user_by_username(request.username)
        if not user:
            raise UserNotFoundException
        if not self._password_service.validate_password(request.password, user.password):
            raise WrongPasswordException

        token_data = TokenData(username=request.username)
        refresh_token = self._token_service.create_refresh_token(token_data)
        access_token = self._token_service.create_access_token(token_data)
        await self._repository.update_refresh_token_by_username(
            JWTToken(username=request.username, refresh_token=refresh_token)
        )

        return CredentialsResponse(access_token=access_token, refresh_token=refresh_token)
