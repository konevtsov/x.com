from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class PostSchema(BaseModel):
    id: int
    text: str = Field(max_length=280)
    likes_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostCreateRequestSchema(BaseModel):
    text: str = Field(max_length=280)


class PostCreateSchema(BaseModel):
    user_id: int
    author_username: str
    text: str = Field(max_length=280)


class PostDeleteRequestSchema(BaseModel):
    post_id: int


class PostDeleteSchema(BaseModel):
    user_id: int
    post_id: int
