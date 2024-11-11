from fastapi import status

from .base_exception import BaseExceptions


class UserAlreadyExists(BaseExceptions):
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = "User already exists"


class UserNotFound(BaseExceptions):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "User not found"


class InvalidLoginPassword(BaseExceptions):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Invalid login or password"


class Unauthorized(BaseExceptions):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "User is not authorized"


class InvalidTokenType(BaseExceptions):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Invalid token type"


class InvalidToken(BaseExceptions):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Invalid token"
