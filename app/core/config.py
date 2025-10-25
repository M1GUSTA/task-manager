from dataclasses import dataclass

from dotenv import find_dotenv
from environs import Env
from pydantic_settings import BaseSettings, SettingsConfigDict


@dataclass
class DatabaseConfig:
    database_url: str


@dataclass
class Config:
    db: DatabaseConfig
    secret_key: str
    debug: bool


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        db=DatabaseConfig(database_url=env("DATABASE_URL")),
        secret_key=env("SECRET_KEY"),
        debug=env.bool("DEBUG", default=False),
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
    )

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
