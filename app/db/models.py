import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    completed: Mapped[bool] = mapped_column(default=False)
    completed_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    creator_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    creator: Mapped["User"] = relationship("User", foreign_keys=[creator_id], back_populates="created_tasks")

    assignee_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    assignee: Mapped["User | None"] = relationship("User", foreign_keys=[assignee_id], back_populates="assigned_tasks")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    sign_up: Mapped[bool] = mapped_column(default=False)

    created_tasks: Mapped[list["Task"]] = relationship("Task", foreign_keys="Task.creator_id", back_populates="creator")

    assigned_tasks: Mapped[list["Task"]] = relationship(
        "Task", foreign_keys="Task.assigned_id", back_populates="assignee"
    )
