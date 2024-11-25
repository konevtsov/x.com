from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    username: str
    name: str
    email: EmailStr
    is_active: bool
    bio: str
    website: str
    is_banned: bool
