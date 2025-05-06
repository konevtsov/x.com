import uuid
from datetime import UTC, datetime, timedelta

import jwt

from configuration.config import settings


class JWTService:
    @staticmethod
    def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(UTC)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
            jti=str(uuid.uuid4()),
        )
        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
        return encoded

    @staticmethod
    def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
    ) -> dict:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return decoded
