import aiohttp
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from fastapi.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

logger.add(
    "src/logs/debug.log",
    format="{time} - {level} - {message}",
    level="INFO",
    rotation="5 MB",
    compression="zip"
)


class DbSettings(BaseSettings):
    db_host: str = Field(json_schema_extra={'env': 'DB_HOST'})
    db_user: str = Field(json_schema_extra={'env': 'DB_USER'})
    db_pass: str = Field(json_schema_extra={'env': 'DB_PASS'})
    db_name: str = Field(json_schema_extra={'env': 'DB_NAME'})
    db_port: int = Field(json_schema_extra={'env': 'DB_PORT'})

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="ignore")

    @property
    def dsn(self):
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def dsn_asyncmy(self):
        return f"mysql+asyncmy://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def dsn_asyncpg(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"


class JWTConfig(BaseSettings):
    refresh_token_name: str = Field(json_schema_extra={'env': 'JWT_REFRESH_TOKEN_NAME'})
    access_token_name: str = Field(json_schema_extra={'env': 'JWT_ACCESS_TOKEN_NAME'})
    private_key_path: Path = BASE_DIR / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'jwt-public.pem'
    algorithm: str = Field(json_schema_extra={'env': 'JWT_ALGORITHM'})

    model_config = SettingsConfigDict(env_prefix="JWT_", env_file=".env", extra="ignore")


class Settings(BaseSettings):
    app_port: int = Field(json_schema_extra={'env': 'APP_PORT'})
    sentry_url: str = Field(json_schema_extra={'env': 'APP_SENTRY_URL'})

    db: DbSettings
    jwt: JWTConfig

    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")


class SessionManager:
    _instance = None

    def __init__(self):
        if SessionManager._instance is None:
            self._session = None
            SessionManager._instance = self

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    async def get_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close_session(self):
        if self._session is not None:
            await self._session.close()
            self._session = None


templates = Jinja2Templates(directory="src/templates")

session_manager = SessionManager.get_instance()

settings = Settings(
    db=DbSettings(),
    jwt=JWTConfig()
)
