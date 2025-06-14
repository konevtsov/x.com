__all__ = ("api_router",)
from fastapi import APIRouter

from configuration.config import settings

from .v1 import v1_router

api_router = APIRouter()
api_router.include_router(v1_router)
