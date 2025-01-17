from pydantic import BaseModel, Field


class Post(BaseModel):
    author: str
    author_username: str
    text: str = Field(max_length=280)
    comment_count: int
    like_count: int
    views_count: int


class PostCreateRequestSchema(BaseModel):
    text: str = Field(max_length=280)


class PostCreateSchema(BaseModel):
    author_email: str
    author_username: str
    text: str = Field(max_length=280)
