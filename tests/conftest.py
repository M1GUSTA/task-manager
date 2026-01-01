from unittest.mock import AsyncMock

import pytest

from app.services.task_service import TaskService
from app.services.user_service import UserService
from app.utils.unitofwork import UnitOfWork


@pytest.fixture
def user_service(mock_uow):
    return UserService(uow=mock_uow)


@pytest.fixture
def user():
    class User:
        id = 1

    return User()


@pytest.fixture
def mock_uow(mocker):
    uow = AsyncMock(spec=UnitOfWork)
    uow.__aenter__.return_value = uow
    uow.__aexit__.return_value = False

    uow.tasks = AsyncMock()
    uow.users = AsyncMock()
    return uow


@pytest.fixture
def task_service(mock_uow):
    return TaskService(mock_uow)
