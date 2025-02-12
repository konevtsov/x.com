from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class FullUserSchema(BaseModel):
    username: str
    name: Optional[str] = None  # TODO: Change to required
    email: EmailStr
    bio: Optional[str] = None
    website: Optional[str] = None
    is_banned: bool
    created_at: datetime
    followers_count: int
    followings_count: int

    model_config = ConfigDict(from_attributes=True)


class PartialUserSchema(BaseModel):
    username: str
    name: Optional[str] = None  # TODO: Change to required
    bio: Optional[str] = None
    website: Optional[str] = None
    created_at: datetime
    followers_count: int
    followings_count: int

    model_config = ConfigDict(from_attributes=True)


class UserUpdateSchema(BaseModel):
    username: str
    name: str
    bio: str
    website: str


class FollowSchema(BaseModel):
    followed_username: str
    follower_id: int


class UnfollowSchema(BaseModel):
    followed_username: str
    follower_id: int


class AvatarUploadSchema(BaseModel):
    content: bytes
    file_extension: str


class DeleteAvatarSchema(BaseModel):
    user_id: int


class GetAvatarSchema(BaseModel):
    username: str
