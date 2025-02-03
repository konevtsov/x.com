from .base_exception import BaseException


class InvalidTokenError(BaseException):
    status_code: int = 403
    detail: str = "Invalid token"
