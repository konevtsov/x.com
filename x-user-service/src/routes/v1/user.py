from fastapi import APIRouter, Depends

from schemas.user import UserUpdateRequestSchema
from services import user_service
from services.user_service import UserService
from .token_introspection import get_token_info_from_current_user
from schemas.token import TokenIntrospectSchema

router = APIRouter(tags=["Users"])


@router.get(
    path="/{username}",
)
async def get_user_by_username(
    username: str,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    user_service: UserService = Depends(UserService),
):
    return await user_service.get_user_by_username(username=username, user_token=user_token)


@router.put(
    path="/",
)
async def update_user(
    user_update: UserUpdateRequestSchema,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    user_service: UserService = Depends(UserService),
):
    await user_service.update_user(user_update, user_token)
