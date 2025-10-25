from . import TaskService, UnitOfWork, UserService


async def get_user_service() -> UserService:
    return UserService(uow=UnitOfWork())


async def get_task_service() -> TaskService:
    return TaskService(uow=UnitOfWork())
