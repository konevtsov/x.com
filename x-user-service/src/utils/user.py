from aiohttp import ClientSession
from pydantic import BaseModel
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from configuration.config import settings


class InvalidTokenError(Exception):
    pass


class TokenIntrospect(BaseModel):
    username: str


http_bearer = HTTPBearer()


async def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    jwt_token = credentials.credentials
    headers = {'Authorization': f'Bearer {jwt_token}'}
    async with ClientSession() as session:
        async with session.get(
            url=settings.auth_api.introspect_url,
            headers=headers,
        ) as response:
            if not response.ok:
                raise InvalidTokenError
            return TokenIntrospect(**await response.json())

