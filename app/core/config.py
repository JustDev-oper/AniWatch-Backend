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
    database_url: str = os.getenv("DATABASE_URL", "")

    # API key для защиты маршрутов. На Railway задайте переменную окружения API_KEY
    # в разделе Secrets/Environment variables и не храните её в репозитории.
    api_key: str = os.getenv("API_KEY", "")

    # S3 / object storage settings (optional). If s3_enabled is True, uploads will
    # be stored in the specified bucket. On Railway you should set these values
    # as environment secrets (S3_ENABLED, S3_BUCKET, S3_REGION, S3_ACCESS_KEY_ID,
    # S3_SECRET_ACCESS_KEY, S3_ENDPOINT_URL, S3_PUBLIC_URL).
    s3_enabled: bool = os.getenv("S3_ENABLED", "false").lower() in ("1", "true", "yes")
    s3_bucket: str = os.getenv("S3_BUCKET", "")
    s3_region: str = os.getenv("S3_REGION", "")
    s3_access_key_id: str = os.getenv("S3_ACCESS_KEY_ID", "")
    s3_secret_access_key: str = os.getenv("S3_SECRET_ACCESS_KEY", "")
    s3_endpoint_url: str = os.getenv("S3_ENDPOINT_URL", "")
    # Optional public base URL used to construct final URLs. If empty, one will
    # be constructed using standard S3 patterns.
    s3_public_url: str = os.getenv("S3_PUBLIC_URL", "")

    class Config:
        env_file = ".env"


settings = Settings()
