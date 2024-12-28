from fastapi import status

from .base_exception import BaseExceptions


class UserNotFoundError(BaseExceptions):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "User not found"
