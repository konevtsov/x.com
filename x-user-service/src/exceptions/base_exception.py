from fastapi import HTTPException


class BaseException(HTTPException):
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
