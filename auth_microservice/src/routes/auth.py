from pydantic import BaseModel
from fastapi import Depends, APIRouter, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from schemas.auth import (
    SignUpRequest,
    SignInRequest,
    CredentialsResponse,
)
from services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])

http_bearer = HTTPBearer()


@router.post(
    "/SignUp/",
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
    response_model=CredentialsResponse,
)
async def sign_up(
    request: SignUpRequest,
    auth_service: AuthService = Depends(AuthService),
):
    return await auth_service.sign_up(request)


@router.post(
    "/SignIn/",
    status_code=status.HTTP_200_OK,
    summary="Вход в аккаунт",
    response_model=CredentialsResponse,
    responses={
        200: {"model": CredentialsResponse},
        401: {"description": "Invalid username or password"},
        404: {"description": "User not found"},
    },
)
async def sign_in(
    request: SignInRequest,
    auth_service: AuthService = Depends(AuthService),
):
    return await auth_service.sign_in(request)


@router.post(
    "/SignOut",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Выход из аккаунта",
)
async def sign_out(
    auth_service: AuthService = Depends(AuthService),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentials.credentials
    await auth_service.sign_out(token)
