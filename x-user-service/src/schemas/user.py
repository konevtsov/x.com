from typing import Any
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
    followers_count: Any
    followings_count: Any

    model_config = ConfigDict(from_attributes=True)


class PartialUserSchema(BaseModel):
    username: str
    name: Optional[str] = None  # TODO: Change to required
    bio: Optional[str] = None
    website: Optional[str] = None
    created_at: datetime
    followers_count: Any
    followings_count: Any

    model_config = ConfigDict(from_attributes=True)


class UserUpdateRequestSchema(BaseModel):
    username: str
    name: str
    bio: str
    website: str


class FollowRequestSchema(BaseModel):
    username: str


class UnfollowRequestSchema(BaseModel):
    username: str


class FollowSchema(BaseModel):
    followed_username: str
    follower_username: str


class UnfollowSchema(BaseModel):
    followed_username: str
    follower_username: str
