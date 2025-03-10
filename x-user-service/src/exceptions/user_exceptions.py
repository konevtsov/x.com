from .base_exception import BaseException


class UserNotFoundError(BaseException):
    status_code: int = 404
    detail: str = "User not found"


class AvatarNotFoundError(BaseException):
    status_code: int = 404
    detail: str = "Avatar not found"


class UsernameAlreadyExistsError(BaseException):
    status_code: int = 409
    detail: str = "Username already exists"


class FollowYourselfError(BaseException):
    status_code: int = 409
    detail: str = "You can't follow yourself"


class UnfollowYourselfError(BaseException):
    status_code: int = 409
    detail: str = "You can't unfollow yourself"


class AlreadyFollowedError(BaseException):
    status_code: int = 409
    detail: str = "You already followed on this user"
