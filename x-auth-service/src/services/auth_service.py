import uuid

from fastapi import Depends

from repositories.refresh_session_repository import RefreshSessionRepository
from .password_service import PasswordService
from repositories.user import UserRepository
from .token_service import (
    TokenService,
    REFRESH_TOKEN_TYPE,
    ACCESS_TOKEN_TYPE,
    TOKEN_SUBJECT_FIELD,
    TOKEN_USERNAME_FIELD,
)
from schemas.auth import (
    SignUpRequestSchema,
    SignInRequestSchema,
    IntrospectResponseSchema,
    JWTTokenUpdateSchema,
    TokenDataSchema,
    TokenResponseSchema, RefreshSessionSchema,
)
from dto.user import UserCreateDTO

from schemas.user import UserCreateSchema
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
        user_repository: UserRepository = Depends(UserRepository),
        refresh_session_repository: RefreshSessionRepository = Depends(RefreshSessionRepository),
        token_service: TokenService = Depends(TokenService),
    ):
        self._user_repository = user_repository
        self._refresh_session_repository = refresh_session_repository
        self._password_service = password_service
        self._token_service = token_service

    async def sign_up(self, request: SignUpRequestSchema) -> None:
        if await self._user_repository.email_exists(request.email):
            raise UserAlreadyExists

        password_hash = self._password_service.hash_password(request.password)
        new_user = UserCreateSchema(
            email=request.email,
            username=request.username,
            password=str(password_hash),
        )
        await self._user_repository.create_user(new_user)

        await user_mq.publish_message(
            data=UserCreateDTO(email=request.email, username=request.username),
            routing_key=MQ_USER_REGISTER_ROUTING_KEY,
        )

    async def sign_in(self, request: SignInRequestSchema) -> TokenResponseSchema:
        user = await self._user_repository.get_user_by_email(request.email)
        if not user:
            raise UserNotFound
        if not self._password_service.validate_password(request.password, user.password):
            raise InvalidLoginPassword

        token_data = TokenDataSchema(email=request.email, username=user.username)
        refresh_token_uuid = str(uuid.uuid4())
        refresh_token = self._token_service.create_refresh_token(token_data)
        access_token = self._token_service.create_access_token(token_data)
        refresh_session_schema = RefreshSessionSchema(
            user_id=user.id, refresh_token_uuid=refresh_token_uuid, refresh_token=refresh_token, ip=request.ip,
        )
        if len(await self._refresh_session_repository.get_all_sessions_by_user_id(user_id=user.id)) >= 5:
            await self._refresh_session_repository.drop_all_sessions(user_id=user.id)
        await self._refresh_session_repository.add_refresh_session(refresh_session_schema)

        return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token_uuid)

    async def sign_out(self, refresh_token_uuid: str) -> None:
        jwt_token = await self._refresh_session_repository.get_token_by_uuid(refresh_token_uuid)
        token_payload = self._token_service.get_token_payload(jwt_token)
        self._token_service.validate_token_type(token_payload, REFRESH_TOKEN_TYPE)

        email = token_payload.get(TOKEN_SUBJECT_FIELD)
        all_refresh_tokens = await self._refresh_session_repository.get_all_refresh_tokens_by_email(email=email)

        if not all_refresh_tokens or jwt_token not in all_refresh_tokens:
            raise Unauthorized
        await self._refresh_session_repository.delete_session_by_uuid(refresh_token_uuid)

    async def refresh(self, refresh_token_uuid: str) -> TokenResponseSchema:
        """
        Refresh access token
        :param refresh_token_uuid: JWT token uuid from cookie
        :return: New access and refresh tokens
        """
        jwt_token = await self._refresh_session_repository.get_token_by_uuid(refresh_token_uuid)
        token_payload = self._token_service.get_token_payload(jwt_token)
        self._token_service.validate_token_type(token_payload, REFRESH_TOKEN_TYPE)

        email = token_payload.get(TOKEN_SUBJECT_FIELD)
        username = token_payload.get(TOKEN_USERNAME_FIELD)
        all_refresh_tokens = await self._refresh_session_repository.get_all_refresh_tokens_by_email(email=email)

        if not all_refresh_tokens or jwt_token not in all_refresh_tokens:
            raise Unauthorized

        token_data = TokenDataSchema(email=email, username=username)
        access_token = self._token_service.create_access_token(token_data)
        refresh_token = self._token_service.create_refresh_token(token_data)
        await self._refresh_session_repository.update_refresh_token_by_uuid(
            JWTTokenUpdateSchema(uuid=refresh_token_uuid, refresh_token=refresh_token)
        )
        return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token_uuid)

    async def introspect(self, jwt_token: str) -> IntrospectResponseSchema:
        token_payload = self._token_service.get_token_payload(jwt_token)
        self._token_service.validate_token_type(token_payload, ACCESS_TOKEN_TYPE)

        email = token_payload.get(TOKEN_SUBJECT_FIELD)
        username = token_payload.get(TOKEN_USERNAME_FIELD)
        return IntrospectResponseSchema(email=email, username=username)
