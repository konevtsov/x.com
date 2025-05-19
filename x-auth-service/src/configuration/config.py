from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"

BASE_DIR = Path(__file__).parent.parent

env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)


@dataclass
class RunConfig:
    title: str = os.getenv("RUN_TITLE", "X.com Auth")
    host: str = os.getenv("RUN_HOST", "127.0.0.1")
    port: int = int(os.getenv("RUN_PORT", 8001))


@dataclass
class CorsSettings:
    allow_origins: list[str] = field(default_factory=lambda: [
        "http://localhost",
        "http://localhost:8000",
    ])
    allow_credentials: bool = field(default=True)
    allow_methods: list[str] = field(default_factory=lambda: ["*"])
    allow_headers: list[str] = field(default_factory=lambda: ["*"])

    def __post_init__(self):
        env_origins = os.getenv("ALLOW_ORIGINS")
        if env_origins:
            self.allow_origins = [origin.strip() for origin in env_origins.split(",")]


@dataclass
class ApiV1Prefix:
    prefix: str = os.getenv("API_V1_PREFIX", "/v1")
    auth: str = os.getenv("API_V1_AUTH_PREFIX", "/auth")


@dataclass
class ApiPrefix:
    prefix: str = os.getenv("API_PREFIX", "/api")
    v1: ApiV1Prefix = field(default_factory=ApiV1Prefix)


@dataclass
class LoggingConfig:
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = os.getenv("LOGGING_LOG_LEVEL", "INFO")
    log_format: str = LOG_DEFAULT_FORMAT


@dataclass
class AuthJWT:
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    refresh_token_expire_days: int = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", 60))


@dataclass
class RMQConfig:
    user: str = os.getenv("RMQ_USER", "guest")
    password: str = os.getenv("RMQ_PASSWORD", "guest")
    host: str = os.getenv("RMQ_HOST", "localhost")
    port: int = int(os.getenv("RMQ_PORT", 5672))

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}"


@dataclass
class DatabaseConfig:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "")

    echo: bool = bool(os.getenv("DB_ECHO", False))
    echo_pool: bool = bool(os.getenv("DB_ECHO", False))
    pool_size: int = int(os.getenv("DB_POOL_SIZE", 50))
    max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", 10))

    naming_convention: dict[str, str] = field(default_factory=lambda: {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}" \
               f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


@dataclass
class Settings:
    run: RunConfig = field(default_factory=RunConfig)
    cors: CorsSettings = field(default_factory=CorsSettings)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    auth_jwt: AuthJWT = field(default_factory=AuthJWT)
    api: ApiPrefix = field(default_factory=ApiPrefix)
    rmq: RMQConfig = field(default_factory=RMQConfig)
    db: DatabaseConfig = field(default_factory=DatabaseConfig)


settings = Settings()
