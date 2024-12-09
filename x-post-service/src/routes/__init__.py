__all__ = (
    "api_router",
)
from fastapi import APIRouter

from .v1 import v1_router
from configuration.config import settings

api_router = APIRouter()
api_router.include_router(
    v1_router,
    prefix=settings.api.prefix
)
