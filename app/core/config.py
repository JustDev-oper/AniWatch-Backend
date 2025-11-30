"""
Configuration module for AniWatch Backend
"""
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AniWatch Backend"

    # По умолчанию ожидаем MySQL. Если вы хотите использовать SQLite локально,
    # установите переменную окружения DATABASE_URL в нужное значение.
    # Пример MySQL URL (pymysql): mysql+pymysql://user:password@127.0.0.1:3306/anime_db
    database_url: str = os.getenv("DATABASE_URL",
                                  "mysql+pymysql://root:iaMWVnjzaRoQPOmLNhzALvkpVtiJVqXM@interchange.proxy.rlwy.net:46154/railway")

    class Config:
        env_file = ".env"


settings = Settings()
