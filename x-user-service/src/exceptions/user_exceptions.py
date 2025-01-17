from fastapi import status

from .base_exception import BaseExceptions


class UserNotFoundError(BaseExceptions):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "User not found"


class FollowYourselfError(BaseExceptions):
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = "You can't follow yourself"


class UnfollowYourselfError(BaseExceptions):
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = "You can't unfollow yourself"


class AlreadyFollowedError(BaseExceptions):
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = "You already followed on this user"
