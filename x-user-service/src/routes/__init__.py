__all__ = (
    "api_router",
)
from fastapi import APIRouter

from .v1 import api_v1_router
from configuration.config import settings

api_router = APIRouter(
    prefix=settings.api.prefix,
)
api_router.include_router(api_v1_router)
