"""
Database session module for AniWatch Backend
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# Создание движка базы данных
# Поддержка как SQLite (локально), так и MySQL/Postgres через SQLAlchemy URL
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}  # Только для SQLite
    )
else:
    # Для сетевых СУБД (например MySQL через pymysql) полезно включать pool_pre_ping
    # чтобы реконнектиться при «stale» соединениях
    engine = create_engine(
        settings.database_url,
        pool_pre_ping=True
    )

# Создание локальной сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


def get_db() -> Session:
    """
    Зависимость для получения сессии базы данных
    Используется в FastAPI через Depends
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
