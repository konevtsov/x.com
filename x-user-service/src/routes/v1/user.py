from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse

from schemas.user import (
    FollowSchema,
    UnfollowSchema,
    AvatarUploadSchema,
    UserUpdateSchema,
    DeleteAvatarSchema,
    GetAvatarSchema,
)
from .user_schemas import (
    UserUpdateRequestSchema,
    FollowRequestSchema,
    UnfollowRequestSchema,
)
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
    path="/{username}/followers",
)
async def get_followers_by_username(
    username: str,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    user_service: UserService = Depends(UserService),
):
    return await user_service.get_followers_by_username(username=username)


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
        follower_id=user_token.user_id,
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
        follower_id=user_token.user_id,
    )
    await user_service.unfollow(unfollow_schema=unfollow_schema)


@router.post(
    path="/avatar",
)
async def upload_avatar(
    file: UploadFile,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    user_service: UserService = Depends(UserService),
):
    allowed_content_types = ["image/jpeg"]
    if file.content_type not in allowed_content_types:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported Content-Type")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")

    file_extension = str(file.content_type.split('/')[1])
    upload_avatar_schema = AvatarUploadSchema(content=content, file_extension=file_extension)
    await user_service.upload_avatar(upload_schema=upload_avatar_schema, user_token=user_token)


@router.get(
    path="/{username}/avatar",
)
async def get_avatar(
    username: str,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    user_service: UserService = Depends(UserService),
):
    get_avatar_schema = GetAvatarSchema(username=username)
    data = await user_service.get_avatar_by_username(get_avatar_schema)
    return StreamingResponse(iter([data]), media_type="image/jpeg")


@router.delete(
    path="/avatar",
)
async def delete_avatar(
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    user_service: UserService = Depends(UserService),
):
    delete_avatar_schema = DeleteAvatarSchema(user_id=user_token.user_id)
    await user_service.delete_avatar(delete_avatar_schema)


@router.put(
    path="/",
)
async def update_user(
    user_update: UserUpdateRequestSchema,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    user_service: UserService = Depends(UserService),
):
    user_update_schema = UserUpdateSchema(
        username=user_update.username,
        name=user_update.name,
        bio=user_update.bio,
        website=user_update.website,
    )
    await user_service.update_user(user_update_schema, user_token)
