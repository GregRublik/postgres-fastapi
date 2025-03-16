import aiohttp
from authx import AuthXConfig, AuthX
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from fastapi.templating import Jinja2Templates

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


# class JWTConfig(AuthXConfig):
#     JWT_SECRET_KEY: int = Field(json_schema_extra={'env': 'JWT_SECRET_KEY'})
#     JWT_ACCESS_COOKIE_NAME: str = Field(json_schema_extra={'env': 'JWT_ACCESS_COOKIE_NAME'})
#     JWT_TOKEN_LOCATION: str = Field(json_schema_extra={'env': 'JWT_TOKEN_LOCATION'})
#
#     model_config = SettingsConfigDict(env_prefix="JWT_", env_file=".env", extra="ignore")


class Settings(BaseSettings):
    app_port: int = Field(json_schema_extra={'env': 'APP_PORT'})
    sentry_url: str = Field(json_schema_extra={'env': 'APP_SENTRY_URL'})

    db: DbSettings
    security: AuthX

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

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_COOKIE_NAME = "my_secret_key"

settings = Settings(
    db=DbSettings(),
    security=AuthX(config=config)
)
