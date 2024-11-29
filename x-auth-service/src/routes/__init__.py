__all__ = (
    "api_router",
)
from fastapi import APIRouter

from configuration.config import settings
from .v1 import api_v1_router

api_router = APIRouter(
    prefix=settings.api.prefix,
)
api_router.include_router(api_v1_router)
