__all__ = ("api_v1_router",)
from fastapi import APIRouter

from configuration.config import settings

from .user import router as user_router

api_v1_router = APIRouter(
    prefix=settings.api.v1.prefix,
)
api_v1_router.include_router(
    router=user_router,
    prefix=settings.api.v1.users,
    tags=["Users"],
)
