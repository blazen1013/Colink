from functools import lru_cache
from typing import List

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    app_name: str = "Colink Employee Service"
    database_url: str = "mysql+pymysql://user:password@localhost:3306/collab_platform"
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    @validator("cors_origins", pre=True)
    def parse_origins(cls, value):  # type: ignore[override]
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
