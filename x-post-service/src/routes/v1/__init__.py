__all__ = (
    "v1_router",
)
from fastapi import APIRouter

from configuration.config import settings
from .post import router as post_router

v1_router = APIRouter(prefix=settings.api.v1.prefix)
v1_router.include_router(post_router, prefix=settings.api.v1.posts)
