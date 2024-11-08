from pydantic import BaseModel


class SignUpRequest(BaseModel):
    username: str
    password: str


class SignInRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    refresh_token: str | None = None
    access_token: str
    token_type: str = "Bearer"


class JWTTokenUpdate(BaseModel):
    username: str
    refresh_token: str


class TokenData(BaseModel):
    username: str
