from fastapi import Depends, APIRouter, status
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from schemas.auth import (
    SignUpRequestSchema,
    SignInRequestSchema,
    IntrospectResponseSchema,
    TokenResponseSchema,
)
from services.auth_service import AuthService

router = APIRouter()

http_bearer = HTTPBearer()


@router.post(
    "/SignUp/",
    status_code=status.HTTP_201_CREATED,
    summary="Sign up new account",
    responses={
        201: {"description": "User created successfully"},
    }
)
async def sign_up(
    request: SignUpRequestSchema,
    auth_service: AuthService = Depends(AuthService),
):
    return await auth_service.sign_up(request)


@router.post(
    "/SignIn/",
    status_code=status.HTTP_200_OK,
    summary="Sign in to account",
    response_model=TokenResponseSchema,
    responses={
        200: {"model": TokenResponseSchema},
        401: {"description": "Invalid username or password"},
        404: {"description": "User not found"},
    },
)
async def sign_in(
    request: SignInRequestSchema,
    auth_service: AuthService = Depends(AuthService),
):
    return await auth_service.sign_in(request)


@router.post(
    "/SignOut/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Sign out from account",
    responses={
        401: {"description": "Invalid token type"},
        403: {"description": "Not authorized"},
    }
)
async def sign_out(
    auth_service: AuthService = Depends(AuthService),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    jwt_token = credentials.credentials
    await auth_service.sign_out(jwt_token)


@router.post(
    "/Refresh/",
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    response_model=TokenResponseSchema,
    response_model_exclude_none=True,
    responses={
        401: {"description": "User is not authorized"},
    }
)
async def refresh(
    auth_service: AuthService = Depends(AuthService),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    jwt_token = credentials.credentials
    return await auth_service.refresh(jwt_token)


@router.get(
    path="/Introspect/",
    status_code=status.HTTP_200_OK,
    summary="Token introspection",
    response_model=IntrospectResponseSchema,
    responses={
        200: {"model": IntrospectResponseSchema},
        401: {"description": "User is not authorized"},
    }
)
async def introspect(
    auth_service: AuthService = Depends(AuthService),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    jwt_token = credentials.credentials
    return await auth_service.introspect(jwt_token)
