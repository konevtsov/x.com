from fastapi import UploadFile
from pydantic import BaseModel


class AvatarUploadRequestSchema(BaseModel):
    file: UploadFile


class UserUpdateRequestSchema(BaseModel):
    username: str
    name: str
    bio: str
    website: str


class FollowRequestSchema(BaseModel):
    username: str


class UnfollowRequestSchema(BaseModel):
    username: str
