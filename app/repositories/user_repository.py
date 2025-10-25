from app.repositories.base_repository import Repository

from . import User, select


class UserRepository(Repository):
    model = User

    async def find_by_username(self, username: str):
        stmt = select(self.model).filter(self.model.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
