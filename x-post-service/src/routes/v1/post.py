from fastapi import APIRouter, Depends

from schemas.post import PostCreateRequestSchema, PostCreateSchema, PostDeleteRequestSchema, PostDeleteSchema
from schemas.token import TokenIntrospectSchema
from services.post_service import PostService
from .token_introspection import get_token_info_from_current_user

router = APIRouter(tags=["Post"])


@router.get(
    "/{username}",
)
async def get_all_posts_by_username(
    username: str,
    user_token: str = Depends(get_token_info_from_current_user),
    post_service: PostService = Depends(PostService),
):
    return await post_service.get_all_posts_by_username(username=username)


@router.get(
    "/status/{post_id}",
)
async def get_post_by_id(
    post_id: int,
    user_token: str = Depends(get_token_info_from_current_user),
    post_service: PostService = Depends(PostService),
):
    return await post_service.get_post_by_id(post_id=post_id)


@router.post(
    "/",
)
async def post_create(
    post_create_req: PostCreateRequestSchema,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    post_service: PostService = Depends(PostService),
):
    post_create_schema = PostCreateSchema(
        user_id=user_token.user_id,
        author_username=user_token.username,
        text=post_create_req.text,
    )
    await post_service.create_post(post_create_schema)


@router.delete(
    "/",
)
async def post_delete(
    post_delete_req: PostDeleteRequestSchema,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    post_service: PostService = Depends(PostService),
):
    post_delete_schema = PostDeleteSchema(
        user_id=user_token.user_id,
        post_id=post_delete_req.post_id,
    )
    await post_service.delete_post(post_delete_schema)
