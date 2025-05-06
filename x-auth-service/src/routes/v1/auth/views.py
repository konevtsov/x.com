from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import ORJSONResponse
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from schemas.auth import (
    IntrospectResponseSchema,
    SignInRequest,
    SignInRequestSchema,
    SignUpRequestSchema,
    TokenResponseSchema,
)
from services.auth_service import AuthService

router = APIRouter()

http_bearer = HTTPBearer()

REFRESH_TOKEN_ALIAS = "refresh_token"


@router.post(
    "/SignUp/",
    status_code=status.HTTP_201_CREATED,
    summary="Sign up new account",
    responses={
        201: {"description": "User created successfully"},
    },
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
    req: Request,
    request: SignInRequest,
    auth_service: AuthService = Depends(AuthService),
):
    ip = req.client.host
    request_schema = SignInRequestSchema(
        email=request.email,
        password=request.password,
        ip=ip,
    )
    tokens_data = await auth_service.sign_in(request_schema)
    response = ORJSONResponse(
        content={
            "data": {
                "access_token": tokens_data.access_token,
                "refresh_token": tokens_data.refresh_token,
            }
        }
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens_data.refresh_token,
        httponly=True,
        secure=True,
    )
    return response


@router.post(
    "/SignOut/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Sign out from account",
    responses={
        401: {"description": "Invalid token type"},
        403: {"description": "Not authorized"},
    },
)
async def sign_out(
    request: Request,
    auth_service: AuthService = Depends(AuthService),
):
    refresh_token_uuid = request.cookies.get(REFRESH_TOKEN_ALIAS)
    await auth_service.sign_out(refresh_token_uuid)


@router.post(
    "/Refresh/",
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    response_model=TokenResponseSchema,
    response_model_exclude_none=True,
    responses={
        401: {"description": "User is not authorized"},
    },
)
async def refresh(
    request: Request,
    auth_service: AuthService = Depends(AuthService),
):
    refresh_token_uuid = request.cookies.get(REFRESH_TOKEN_ALIAS)
    return await auth_service.refresh(refresh_token_uuid)


@router.get(
    path="/Introspect/",
    status_code=status.HTTP_200_OK,
    summary="Token introspection",
    response_model=IntrospectResponseSchema,
    responses={
        200: {"model": IntrospectResponseSchema},
        401: {"description": "User is not authorized"},
    },
)
async def introspect(
    auth_service: AuthService = Depends(AuthService),
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    jwt_token = credentials.credentials
    return await auth_service.introspect(jwt_token)
