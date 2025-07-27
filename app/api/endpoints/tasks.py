from fastapi import APIRouter

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.get("/")
async def get_tasks():
    pass


@task_router.post("/")
async def create_todo():
    pass
