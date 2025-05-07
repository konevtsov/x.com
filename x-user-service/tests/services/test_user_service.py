from unittest.mock import AsyncMock

import pytest

from dto.user import UserCreateDTO
from exceptions.user_exceptions import (
    UserNotFoundError,
)
from repositories.user_repository import UserRepository
from schemas.token import TokenIntrospectSchema
from schemas.user import UserUpdateSchema
from services.user_service import UserService


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
    mock_user_repository.get_username_exist_count = AsyncMock(return_value=1)
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
    mock_user_repository.get_username_exist_count.return_value = 2
    with pytest.raises(UserNotFoundError) as exc_info:
        await user_service.update_user(user_update, user_token)
    assert exc_info.value.status_code == 404
