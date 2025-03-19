from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class ServiceApiModel(BaseModel):
    PREDICT_SECRET: str = '123'
    PREDICT_URL: str = "http://0.0.0.0:8016"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=Path(BASE_DIR, ".env"),
        env_nested_delimiter="__",
    )
    HOST: str = "0.0.0.0"
    PORT: int = 8083

    DEBUG: int = 1

    MONGO_URL: str
    MONGO_DB_NAME: str

    RABBIT_URL: str
    EXCHANGE_RABBIT_NAME: str

    service: ServiceApiModel = ServiceApiModel()


settings = Settings()  # type: ignore
