from fastapi import HTTPException, status


class BaseExceptions(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
        )


class PermissionDeniedError(BaseExceptions):
    status_code: int = status.HTTP_403_FORBIDDEN
    detail: str = "Permission denied"
