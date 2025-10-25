from sqlalchemy import delete, insert, select, update

from app.repositories.base_repository import Repository

from . import Task


class TaskRepository(Repository):
    model = Task

    async def find_all(self, user):
        stmt = select(self.model).where(self.model.creator_id == user.id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def find_one(self, id: int):
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)

        return result.scalar_one()

    async def update(self, id: int, data: dict):
        stmt = update(self.model).where(self.model.id == id).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, id: int):
        stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
        result = await self.session.execute(stmt)
        deleted_id = result.scalar_one_or_none()
        return deleted_id is not None
