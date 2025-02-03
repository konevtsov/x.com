from pydantic import BaseModel, EmailStr


class SignUpRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpRequestSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class SignInRequestSchema(BaseModel):
    email: EmailStr
    password: str
    ip: str


class IntrospectResponseSchema(BaseModel):
    user_id: int
    username: str


class TokenResponseSchema(BaseModel):
    refresh_token: str | None = None
    access_token: str
    token_type: str = "Bearer"


class JWTTokenUpdateSchema(BaseModel):
    uuid: str
    refresh_token: str


class TokenDataSchema(BaseModel):
    user_id: int
    username: str


class RefreshSessionSchema(BaseModel):
    user_id: int
    refresh_token_uuid: str
    refresh_token: str
    ip: str
