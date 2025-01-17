from fastapi import APIRouter, Depends

from schemas.post import PostCreateRequestSchema, PostCreateSchema
from schemas.token import TokenIntrospectSchema
from services.post_service import PostService
from .token_introspection import get_token_info_from_current_user

router = APIRouter(tags=["Post"])


@router.post(
    "/",
)
async def post_create(
    post_create_req: PostCreateRequestSchema,
    user_token: TokenIntrospectSchema = Depends(get_token_info_from_current_user),
    post_service: PostService = Depends(PostService),
):
    post_create_schema = PostCreateSchema(
        author_email=user_token.email,
        author_username=user_token.username,
        text=post_create_req.text
    )
    return await post_service.create_post(post_create_schema)
