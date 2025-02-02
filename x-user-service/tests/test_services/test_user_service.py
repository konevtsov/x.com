import pytest

from unittest.mock import AsyncMock

from src.services.user_service import UserService
from src.schemas.token import TokenIntrospectSchema
from src.schemas.user import UserUpdateRequestSchema, FollowSchema, UnfollowSchema
from src.exceptions.user_exceptions import (
    UserNotFoundError,
    FollowYourselfError,
    UnfollowYourselfError,
    AlreadyFollowedError,
)
from src.dto.user import UserCreateDTO
from src.repositories.user_repository import UserRepository, UserCreateDTO


@pytest.fixture
def mock_user_repository():
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repository):
    return UserService(repository=mock_user_repository)


@pytest.mark.asyncio
async def test_create_user(user_service, mock_user_repository):
    user_data = UserCreateDTO(email="test@example.com", username="test_username")
    await user_service.create_user(user=user_data)
    mock_user_repository.create_user.assert_called_once_with(user=user_data)


@pytest.mark.asyncio
async def test_update_user_good(user_service, mock_user_repository):
    user_update = UserUpdateRequestSchema(
        username="test_username",
        name="test_name",
        bio="test_bio",
        website="test_website",
    )
    user_token = TokenIntrospectSchema(email="test@example.com", username="test_username")
    mock_user_repository.get_user_by_email.return_value = AsyncMock()
    await user_service.update_user(user_update, user_token)
    mock_user_repository.update_user_by_email.assert_awaited_once_with(user_update, email=user_token.email)


@pytest.mark.asyncio
async def test_update_user_bad(user_service, mock_user_repository):
    user_update = UserUpdateRequestSchema(
        username="test_username",
        name="test_name",
        bio="test_bio",
        website="test_website",
    )
    user_token = TokenIntrospectSchema(email="test@example.com", username="test_username")
    mock_user_repository.get_user_by_email.return_value = None
    with pytest.raises(UserNotFoundError) as exc_info:
        await user_service.update_user(user_update, user_token)
        assert exc_info.value.status_code == 404
