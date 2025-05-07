from fastapi import status

from .base_exception import BaseExceptions


class PostNotFoundError(BaseExceptions):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "Post not found"
