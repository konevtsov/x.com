from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    email: EmailStr
    username: str
