__all__ = (
    "v1_router",
)
from fastapi import APIRouter

from configuration.config import settings

v1_router = APIRouter(prefix=settings.api.v1.prefix)
