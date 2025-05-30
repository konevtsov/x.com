__all__ = ("api_v1_router",)
from fastapi import APIRouter

from configuration.config import settings

from .auth import auth_router

api_v1_router = APIRouter(
    prefix=settings.api.v1.prefix,
)

api_v1_router.include_router(
    router=auth_router,
    tags=["Auth"],
)
