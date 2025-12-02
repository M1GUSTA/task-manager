from unittest.mock import AsyncMock

import pytest

from app.api.schemas.user import UserCreate
from app.exceptions.exceptions import UsernameAlreadyExists


@pytest.mark.asyncio
async def test_add_user(user_service, mock_uow):
    user = UserCreate(username="john", email="j@e.com", password="hash")

    mock_uow.users.add.return_value = {"id": 1, "username": "john", "email": "e@e.com", "password": "hash"}

    new_user = await user_service.add(user)

    assert new_user.id == 1
    mock_uow.users.add.assert_called_once()


@pytest.mark.asyncio
async def test_add_user_username_exists(user_service, mock_uow):
    user = UserCreate(username="john", email="e@e.com", password="hash")

    user_service.find_by_username = AsyncMock(return_value=True)

    with pytest.raises(UsernameAlreadyExists):
        await user_service.add(user)
