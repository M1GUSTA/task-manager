from pydantic import BaseModel
from datetime import datetime


class Task(BaseModel):
    id: int
    name: str
    text: str
    create_date:  datetime | datetime.date.now
    is_complete: bool = False
    complete_date: datetime | None = None
    creator: str
    