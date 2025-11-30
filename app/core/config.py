"""
Configuration module for AniWatch Backend
"""
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AniWatch Backend"
    version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"

    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./anilist.db")

    class Config:
        env_file = ".env"


settings = Settings()
