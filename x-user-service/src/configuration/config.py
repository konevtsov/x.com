from typing import Literal
from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    title: str = "X.com User"
    host: str = "127.0.0.1"
    port: int = 8001


class CorsSettings(BaseModel):
    allow_origins: list[str] = [
        "http://localhost",
        "http://localhost:8000",
    ]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class AuthApi(BaseModel):
    base_url: str = "http://localhost:8001/api/v1"
    introspect_path: str = "/auth/Introspect/"

    @property
    def introspect_url(self) -> str:
        return self.base_url + self.introspect_path


class LoggingConfig(BaseModel):
    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str = LOG_DEFAULT_FORMAT


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class RMQConfig(BaseModel):
    user: str = "guest"
    password: str = "guest"
    host: str = "localhost"
    port: int = 5672

    url: str = f"amqp://{user}:{password}@{host}:{port}/"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env.dist",
            BASE_DIR / ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    cors: CorsSettings = CorsSettings()
    logging: LoggingConfig = LoggingConfig()
    rmq: RMQConfig = RMQConfig()
    auth_api: AuthApi = AuthApi()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()
