from datetime import datetime

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(..., max_length=100, example="Fix login page")
    description: str = Field(..., example="Button boesn't work")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class TaskInDB(TaskBase):
    id: int
    creater_id: int
    assignee_id: int | None = None
    created_at: datetime | datetime
    completed: bool = False
    completed_at: datetime | None = None

    class Config:
        orm_mode = True
