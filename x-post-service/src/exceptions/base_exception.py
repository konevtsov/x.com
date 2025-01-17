from fastapi import HTTPException


class BaseExceptions(HTTPException):

    def __init__(self, detail=None):
        self.detail = detail
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
        )
