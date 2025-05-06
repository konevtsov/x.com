from datetime import timedelta

from fastapi import Depends
from jwt.exceptions import InvalidTokenError

from configuration.config import settings
from exceptions.auth_exceptions import (
    InvalidToken,
    InvalidTokenType,
)
from schemas.auth import TokenDataSchema
from services.jwt_service import JWTService

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
TOKEN_SUBJECT_FIELD = "sub"
TOKEN_USERNAME_FIELD = "username"


class TokenService:
    def __init__(self, jwt_service: JWTService = Depends(JWTService)):
        self._jwt_service = jwt_service

    def create_jwt(
        self,
        token_type: str,
        token_data: dict,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        jwt_payload = {TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return self._jwt_service.encode_jwt(
            payload=jwt_payload,
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta,
        )

    def create_access_token(self, data: TokenDataSchema) -> str:
        jwt_payload = {
            "sub": data.user_id,
            "username": data.username,
        }
        return self.create_jwt(
            token_type=ACCESS_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_minutes=settings.auth_jwt.access_token_expire_minutes,
        )

    def create_refresh_token(self, data: TokenDataSchema) -> str:
        jwt_payload = {
            "sub": data.user_id,
            "username": data.username,
        }
        return self.create_jwt(
            token_type=REFRESH_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
        )

    def get_token_payload(self, token: str) -> dict:
        try:
            payload = self._jwt_service.decode_jwt(token=token)
        except InvalidTokenError as exc:
            raise InvalidToken from exc
        return payload

    def validate_token_type(self, payload: dict, token_type: str) -> bool:
        if payload.get(TOKEN_TYPE_FIELD) == token_type:
            return True
        raise InvalidTokenType
