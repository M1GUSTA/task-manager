import pytest

from app.api.schemas.task import TaskCreate
from app.exceptions.exceptions import AccessDeniedError, TaskNotFoundError


@pytest.mark.asyncio
async def test_add_task(task_service, mock_uow, user):
    task = TaskCreate(title="Test", description="Desc")

    mock_uow.tasks.add.return_value = {
        "id": 10,
        "title": "Test",
        "description": "Desc",
        "creator_id": user.id,
        "assigned_id": user.id,
        "created_at": "2025-01-01T00:00:00",
    }

    new_task = await task_service.add(task, user)

    mock_uow.tasks.add.assert_called_once()
    assert new_task.id == 10
    assert new_task.creator_id == user.id


@pytest.mark.asyncio
async def test_find_one_access_denied(task_service, mock_uow, user):
    mock_uow.tasks.find_one.return_value = {"id": 1, "creator_id": 999}

    with pytest.raises(AccessDeniedError):
        await task_service.find_one(1, user)


@pytest.mark.asyncio
async def test_find_one_not_found(task_service, mock_uow, user):
    mock_uow.tasks.find_one.return_value = None

    with pytest.raises(TaskNotFoundError):
        await task_service.find_one(1, user)


@pytest.mark.asyncio
async def test_delete_task(task_service, mock_uow, user):
    mock_uow.tasks.find_one.return_value = {"id": 1, "creator_id": user.id}
    mock_uow.tasks.delete.return_value = True

    result = await task_service.delete(1, user)

    assert result is True
    mock_uow.tasks.delete.assert_called_once()


@pytest.mark.asyncio
async def test_delete_task_access_denied(task_service, mock_uow, user):
    mock_uow.tasks.find_one.return_value = {"id": 1, "creator_id": 999}

    with pytest.raises(AccessDeniedError):
        await task_service.delete(1, user)
