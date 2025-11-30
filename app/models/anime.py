from sqlalchemy import Column, Integer, String, Text, DateTime

from app.database.session import Base


class Anime(Base):
    __tablename__ = 'anime'
    id = Column(Integer, primary_key=True)
    title = Column(String(350), unique=True, nullable=False)
    subtitle = Column(String(100), unique=False, nullable=True)
    description = Column(Text, unique=False, nullable=False)
    preview_image = Column(String(500), unique=False, nullable=False)
    video_url = Column(Text, unique=False, nullable=False)
    created_at = Column(DateTime, unique=False, nullable=False)
    updated_at = Column(DateTime, unique=False, nullable=False)
