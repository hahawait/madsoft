from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")


class DBConfig(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int
    DB_PASS: str
    DB_USER: str

    @property
    def database_url(self):
        user = f"{self.DB_USER}:{self.DB_PASS}"
        database = f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"asyncpg://{user}@{database}"


class StorageConfig(BaseSettings):
    AWS_BUCKET_NAME: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_ACCESS_KEY_ID: str
    AWS_URL: str


class AppConfig(BaseSettings):
    MODE: Literal["PROD", "DEV", "LOCAL"]

    FASTAPI_HOST: str
    FASTAPI_PORT: int

    LOGGING_LEVEL: Literal["DEBUG", "INFO", "WARN", "ERROR", "FATAL"] = "INFO"

    PROJECT_NAME: str
    VERSION: str

    @property
    def is_production(self):
        return self.MODE == "PROD"

    @property
    def is_dev(self):
        return self.MODE == "DEV"


@dataclass
class Config:
    app: AppConfig
    storage: StorageConfig
    db: DBConfig


@lru_cache
def get_config():

    return Config(
        app=AppConfig(),
        storage=StorageConfig(),
        db=DBConfig()
    )
