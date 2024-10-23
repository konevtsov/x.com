from fastapi import Depends, APIRouter

from schemas.auth import (
    SignUpRequest,
    SignInRequest,
    CredentialsResponse,
)
from services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/SignUp/",
    summary="Регистрация нового пользователя",
    response_model=CredentialsResponse,
)
async def sign_up(
    request: SignUpRequest,
    auth_service: AuthService = Depends(AuthService)
):
    return await auth_service.sign_up(request)


@router.post(
    "/SignIn/",
    summary="Вход в аккаунт",
    response_model=CredentialsResponse,
)
async def sign_in(
    request: SignInRequest,
    auth_service: AuthService = Depends(AuthService),
):
    return await auth_service.sign_in(request)
