from fastapi import status

from .base_exception import BaseExceptions


class InvalidTokenError(BaseExceptions):
    status_code: int = status.HTTP_403_FORBIDDEN
    detail: str = "Invalid token"
