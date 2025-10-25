from app.api.schemas.task import TaskCreate, TaskInDB
from app.exceptions.exceptions import AccessDeniedError, TaskNotFoundError
from app.utils.unitofwork import UnitOfWork


class TaskService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def find_all(self, user: dict) -> list[TaskInDB]:
        async with self.uow:
            tasks: list = await self.uow.tasks.find_all(user)
            return [TaskInDB.model_validate(task) for task in tasks]

    async def find_one(self, id: int, user: dict) -> TaskInDB:
        async with self.uow:
            task_data = await self.uow.tasks.find_one(id)

            if not task_data:
                raise TaskNotFoundError("Task not found")

            task = TaskInDB.model_validate(task_data)  # <-- фикс

            if task.creator_id == user.id:
                raise AccessDeniedError()

            return TaskInDB.model_validate(task)

            raise TaskNotFoundError()

    async def add(self, task: TaskCreate, user: dict) -> TaskInDB:
        task_dict: dict = task.model_dump()
        task_dict["creator_id"] = user.id
        task_dict["assigned_id"] = user.id

        async with self.uow:
            task_from_db = await self.uow.tasks.add(task_dict)

            task_to_return = TaskInDB.model_validate(task_from_db)

            await self.uow.commit()

            return task_to_return

    async def update(self, id: int, task: TaskCreate, user: dict) -> TaskInDB:
        task_dict: dict = task.model_dump()

        async with self.uow:
            task = await self.uow.tasks.find_one(id)
            if task:
                if task.creator_id == user.id:
                    task_from_db = await self.uow.tasks.update(id, task_dict)

                    task_to_return = TaskInDB.model_validate(task_from_db)

                    await self.uow.commit()
                    return task_to_return

                raise AccessDeniedError()

            raise TaskNotFoundError()

    async def delete(self, id: int, user: dict) -> bool:
        async with self.uow:
            task: TaskInDB = await self.uow.tasks.find_one(id)

            if task:
                if task.creator_id == user.id:
                    result = await self.uow.tasks.delete(id)
                    await self.uow.commit()

                    return result

                raise AccessDeniedError()

            raise TaskNotFoundError()
