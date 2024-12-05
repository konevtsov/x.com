from fastapi import Depends

from .password_service import PasswordService
from .token_service import (
    TokenService,
    REFRESH_TOKEN_TYPE,
    TOKEN_SUBJECT_FIELD,
)
from repositories.user import UserRepository
from schemas.auth import (
    SignUpRequest,
    SignInRequest,
    TokenResponse,
    JWTTokenUpdate,
    TokenData,
)
from schemas.user import UserSchema, UserOut
from exceptions.auth_exceptions import (
    UserAlreadyExists,
    UserNotFound,
    InvalidLoginPassword,
    Unauthorized,
)
from configuration.rabbitmq.user_queue import (
    user_mq,
    MQ_USER_REGISTER_ROUTING_KEY,
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

    async def sign_up(self, request: SignUpRequest) -> None:
        if await self._repository.username_exists(request.username):
            raise UserAlreadyExists
        if await self._repository.email_exists(request.email):
            raise UserAlreadyExists

        password_hash = self._password_service.hash_password(request.password)
        new_user = UserSchema(
            username=request.username,
            email=request.email,
            password=str(password_hash),
        )
        await self._repository.create_user(new_user)

        user_out = UserOut(
            username=request.username,
            email=request.email,
        )
        await user_mq.publish_message(
            data=user_out,
            routing_key=MQ_USER_REGISTER_ROUTING_KEY,
        )

    async def sign_in(self, request: SignInRequest) -> TokenResponse:
        user = await self._repository.get_user_by_email(request.email)
        if not user:
            raise UserNotFound
        if not self._password_service.validate_password(request.password, user.password):
            raise InvalidLoginPassword

        token_data = TokenData(username=request.username)
        refresh_token = self._token_service.create_refresh_token(token_data)
        access_token = self._token_service.create_access_token(token_data)
        await self._repository.update_refresh_token_by_username(
            JWTTokenUpdate(username=request.username, refresh_token=refresh_token)
        )

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def sign_out(self, jwt_token: str) -> None:
        token_payload = self._token_service.get_token_payload(jwt_token)
        self._token_service.validate_token_type(token_payload, REFRESH_TOKEN_TYPE)

        username = token_payload.get(TOKEN_SUBJECT_FIELD)
        refresh_token = await self._repository.get_token_by_username(username)

        if not refresh_token or refresh_token != jwt_token:
            raise Unauthorized
        await self._repository.delete_token(username)

    async def refresh(self, jwt_token: str) -> TokenResponse:
        """
        Refresh access token
        :param jwt_token: JWT token from Authorization header
        :return: New access token
        """
        token_payload = self._token_service.get_token_payload(jwt_token)
        self._token_service.validate_token_type(token_payload, REFRESH_TOKEN_TYPE)

        username = token_payload.get(TOKEN_SUBJECT_FIELD)
        refresh_token = await self._repository.get_token_by_username(username)

        if not refresh_token or refresh_token != jwt_token:
            raise Unauthorized

        token_data = TokenData(username=username)
        access_token = self._token_service.create_access_token(token_data)
        return TokenResponse(access_token=access_token)
