from pydantic import BaseModel


class TokenIntrospectSchema(BaseModel):
    user_id: int
    username: str
