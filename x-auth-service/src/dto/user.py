from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    user_id: int
    email: EmailStr
    username: str
