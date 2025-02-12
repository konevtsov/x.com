import pytest

from unittest.mock import AsyncMock

from services.user_service import UserService
from schemas.token import TokenIntrospectSchema
from schemas.user import FollowSchema, UnfollowSchema, UserUpdateSchema
from exceptions.user_exceptions import (
    UserNotFoundError,
    FollowYourselfError,
    UnfollowYourselfError,
    AlreadyFollowedError,
)
from dto.user import UserCreateDTO
from repositories.user_repository import UserRepository, UserCreateDTO


@pytest.fixture
def mock_user_repository():
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repository):
    return UserService(repository=mock_user_repository)


@pytest.mark.asyncio
async def test_create_user(user_service, mock_user_repository):
    user_data = UserCreateDTO(email="test@example.com", username="test_username", user_id=1)
    await user_service.create_user(user=user_data)
    mock_user_repository.create_user.assert_called_once_with(user=user_data)


@pytest.mark.asyncio
async def test_update_user_good(user_service, mock_user_repository):
    user_update = UserUpdateSchema(
        username="test_username",
        name="test_name",
        bio="test_bio",
        website="test_website",
    )
    user_token = TokenIntrospectSchema(user_id=1, username="test_username")
    mock_user_repository.get_user_by_user_id.return_value = AsyncMock()
    await user_service.update_user(user_update, user_token)
    mock_user_repository.update_user_by_user_id.assert_awaited_once_with(user_update, user_id=1)


@pytest.mark.asyncio
async def test_update_user_bad(user_service, mock_user_repository):
    user_update = UserUpdateSchema(
        username="test_username",
        name="test_name",
        bio="test_bio",
        website="test_website",
    )
    user_token = TokenIntrospectSchema(user_id=1, username="test_username")
    mock_user_repository.get_user_by_user_id.return_value = None
    with pytest.raises(UserNotFoundError) as exc_info:
        await user_service.update_user(user_update, user_token)
        assert exc_info.value.status_code == 404
