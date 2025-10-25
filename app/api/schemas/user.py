from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserInDB(UserCreate):
    id: int
    sign_up: bool

    class Config:
        from_attributes = True
