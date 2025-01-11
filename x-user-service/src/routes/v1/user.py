from fastapi import APIRouter, Depends

from schemas.user import UserUpdateRequestSchema, FollowRequestSchema, FollowSchema, UnfollowRequestSchema, \
    UnfollowSchema
from services.user_service import UserService
from .token_introspection import get_token_info_from_current_user
from schemas.token import TokenIntrospectSchema

router = APIRouter(tags=["Users"])


@router.get(
    path="/{username}/followings",
)
async def get_followings_by_username(
    username: str,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    user_service: UserService = Depends(UserService),
):
    return await user_service.get_followings_by_username(username=username)


@router.get(
    path="/{username}",
)
async def get_user_by_username(
    username: str,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    user_service: UserService = Depends(UserService),
):
    return await user_service.get_user_by_username(username=username, user_token=user_token)


@router.post(
    path="/follow"
)
async def follow(
    follow_request: FollowRequestSchema,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    user_service: UserService = Depends(UserService),
):
    follow_schema = FollowSchema(
        followed_username=follow_request.username,
        follower_username=user_token.username,
    )
    await user_service.follow(follow_schema=follow_schema)


@router.post(
    path="/unfollow"
)
async def unfollow(
    unfollow_request: UnfollowRequestSchema,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    user_service: UserService = Depends(UserService),
):
    unfollow_schema = UnfollowSchema(
        followed_username=unfollow_request.username,
        follower_username=user_token.username,
    )
    await user_service.unfollow(unfollow_schema=unfollow_schema)


@router.put(
    path="/",
)
async def update_user(
    user_update: UserUpdateRequestSchema,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    user_service: UserService = Depends(UserService),
):
    await user_service.update_user(user_update, user_token)
