from . import ABC, AsyncSession, abstractmethod, insert


# репозиторий - это работа исключительно с бд, без логики.
class AbstractRepository(ABC):
    @abstractmethod
    async def find_all(self):
        # эта ошибка значит "эта функция должна быть реализована в потомке"
        # но пока не реализована
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def add(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self):
        return self.session.query(self.model).all()

    async def find_one(self, id: int):
        return self.session.query(self.model).filter(self.model.id == id).first()

    async def add(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)

        return result.scalar_one()

    async def update(self, id: int, data: dict):
        obj = self.find_one(id)

        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            return obj
        return None

    async def delete(self, id: int):
        obj = self.find_one(id)

        if obj:
            self.session.delete(obj)
            return True
        return False
