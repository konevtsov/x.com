from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    refresh_token: str
