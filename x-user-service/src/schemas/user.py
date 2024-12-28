from pydantic import BaseModel, EmailStr


class UserScheme(BaseModel):
    username: str
    name: str
    email: EmailStr
    is_active: bool
    bio: str
    website: str
    is_banned: bool


class UserUpdateRequestSchema(BaseModel):
    username: str
    name: str
    bio: str
    website: str
