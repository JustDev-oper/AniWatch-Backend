"""
Configuration module for AniWatch Backend
"""
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AniWatch Backend"

    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./anime.db")

    class Config:
        env_file = ".env"


settings = Settings()
