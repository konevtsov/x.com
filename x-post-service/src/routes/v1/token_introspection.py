from aiohttp import ClientSession
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from configuration.config import settings
from exceptions.token_exceptions import InvalidTokenError
from schemas.token import TokenIntrospectSchema

http_bearer = HTTPBearer()


async def get_token_info_from_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    jwt_token = credentials.credentials
    headers = {"Authorization": f"Bearer {jwt_token}"}
    # fmt: off
    async with ClientSession() as session, session.get(
            url=settings.auth_api.introspect_url,
            headers=headers,
        ) as response:
            if not response.ok:
                raise InvalidTokenError
            return TokenIntrospectSchema(**await response.json())
    