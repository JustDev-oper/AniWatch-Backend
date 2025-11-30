"""
Configuration module for AniWatch Backend
"""
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AniWatch Backend"

    # По умолчанию — локальный sqlite (без чувствительных данных).
    # Для production/railway задавайте переменную окружения DATABASE_URL,
    # например: mysql+pymysql://user:password@127.0.0.1:3306/anime_db
    database_url: str = os.getenv("DATABASE_URL",
                                  "mysql+pymysql://root:iaMWVnjzaRoQPOmLNhzALvkpVtiJVqXM@interchange.proxy.rlwy.net:46154/railway")

    # API key для защиты маршрутов. На Railway задайте переменную окружения API_KEY
    # в разделе Secrets/Environment variables и не храните её в репозитории.
    api_key: str = os.getenv("API_KEY", "")

    class Config:
        env_file = ".env"


settings = Settings()
