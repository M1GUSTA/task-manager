from app.api.schemas.user import UserCreate, UserInDB
from app.exceptions.exceptions import UsernameAlreadyExists, UserNotFoundError
from app.utils.unitofwork import UnitOfWork


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def find_all(self) -> list[UserInDB]:
        async with self.uow:
            users: list = await self.uow.users.find_all()
            return [UserInDB.model_validate(user) for user in users]

    async def find_one(self, id: int) -> UserInDB:
        async with self.uow:
            user: UserInDB = await self.uow.users.find_one(id)
            if user:
                return user
            raise UserNotFoundError()

    async def find_by_username(self, username: str) -> UserInDB:
        async with self.uow:
            user: UserInDB = await self.uow.users.find_by_username(username)
            if user:
                return UserInDB.model_validate(user)
            return None

    async def add(self, user: UserCreate) -> UserInDB:
        if not await self.find_by_username(user.username):
            async with self.uow:
                user_dict = {"username": user.username, "email": user.email, "password": user.password}

                user_from_db = await self.uow.users.add(user_dict)
                user_to_return = UserInDB.model_validate(user_from_db)

                await self.uow.commit()

                return user_to_return

        raise UsernameAlreadyExists()

    async def update(self, id: int, user: UserCreate) -> UserInDB:
        user_dict: dict = user.model_dump()

        async with self.uow:
            user_from_db = await self.uow.users.update(id, user_dict)

            if user_from_db:
                user_to_return = UserInDB.model_validate(user_from_db)

                await self.uow.commit()
                return user_to_return

            raise UserNotFoundError()

    async def delete(self, id: int) -> bool:
        async with self.uow:
            result = await self.uow.users.delete(id)

            if result:
                return result
            raise UserNotFoundError()
