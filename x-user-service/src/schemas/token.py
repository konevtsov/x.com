from pydantic import BaseModel


class TokenIntrospectSchema(BaseModel):
    email: str
    username: str
