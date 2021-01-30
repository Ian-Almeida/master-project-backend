from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "master-project"
    DEBUG_MODE: bool = False
    API_STR: str = "/api"


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str
    DB_NAME: str


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
