from pydantic import BaseModel, EmailStr


class SignUpRequestSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class SignInRequestSchema(BaseModel):
    email: EmailStr
    password: str


class IntrospectResponseSchema(BaseModel):
    email: EmailStr
    username: str


class TokenResponseSchema(BaseModel):
    refresh_token: str | None = None
    access_token: str
    token_type: str = "Bearer"


class JWTTokenUpdateSchema(BaseModel):
    email: EmailStr
    refresh_token: str


class TokenDataSchema(BaseModel):
    email: EmailStr
    username: str
