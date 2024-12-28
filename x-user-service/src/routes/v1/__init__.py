__all__ = (
    "api_v1_router",
)
from fastapi import APIRouter

from .user import user_router
from configuration.config import settings


api_v1_router = APIRouter(
    prefix=settings.api.v1.prefix,
)
api_v1_router.include_router(
    router=user_router,
    prefix=settings.api.v1.users,
    tags=["Users"],
)
