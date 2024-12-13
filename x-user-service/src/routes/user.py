from fastapi import APIRouter, Depends

from schemas.user import UserUpdateScheme
from services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.put(
    path="/",
)
async def update_user(
    user: UserUpdateScheme,
    user_service: UserService = Depends(UserService),
):
    await user_service.update_user(user)
