from fastapi import APIRouter, Depends, HTTPException, status

from app.api.endpoints.websocket import manager
from app.api.schemas.task import TaskCreate
from app.core.security import get_current_user
from app.dependencies.dependecies import get_task_service
from app.exceptions.exceptions import AccessDeniedError, TaskNotFoundError
from app.services.task_service import TaskService

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.get("/")
async def get_tasks(
    task_service: TaskService = Depends(get_task_service), current_user: dict = Depends(get_current_user)
):
    return await task_service.find_all(current_user)


@task_router.get("/{task_id}")
async def get_task(
    task_id: int, task_service: TaskService = Depends(get_task_service), current_user: dict = Depends(get_current_user)
):
    try:
        return await task_service.find_one(task_id, current_user)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found") from e

    except AccessDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied") from e


@task_router.post("/")
async def add_task(
    task: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user),
):
    try:
        task = await task_service.add(task, current_user)

        await manager.broadcast(f"\nДобавилась задача: {task.model_dump()}")

        return task
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}") from e


@task_router.put("/{task_id}")
async def update_task(
    task: TaskCreate,
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    current_user: dict = Depends(get_current_user),
):
    try:
        task = await task_service.update(task=task, id=task_id, user=current_user)

        await manager.broadcast(f"\nОбновилась задача: {task.model_dump()}")

        return task

    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found") from e

    except AccessDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied") from e


@task_router.delete("/{task_id}")
async def delete_task(
    task_id: int, task_service: TaskService = Depends(get_task_service), current_user: dict = Depends(get_current_user)
):
    try:
        result = await task_service.delete(task_id, current_user)

        await manager.broadcast(f"\nУдалили задачу с номером: {task_id}")

        return {"success": result}

    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found") from e

    except AccessDeniedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied") from e

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}") from e
