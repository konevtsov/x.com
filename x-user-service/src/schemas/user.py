from pydantic import BaseModel, EmailStr


class UserScheme(BaseModel):
    username: str
    name: str
    email: EmailStr
    is_active: bool
    bio: str
    website: str
    is_banned: bool


class UserUpdateScheme(BaseModel):
    username: str
    name: str
    bio: str
    website: str


class UserInScheme(BaseModel):
    username: str
    email: EmailStr
