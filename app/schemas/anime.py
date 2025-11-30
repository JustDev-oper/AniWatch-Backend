from datetime import datetime

from pydantic import BaseModel


class Anime(BaseModel):
    id: int
    title: str
    subtitle: str = None
    description: str
    preview_image: str
    video_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnimeCreate(BaseModel):
    title: str
    subtitle: str = None
    description: str
    preview_image: str
    video_url: str


class AnimeUpdate(BaseModel):
    title: str = None
    subtitle: str = None
    description: str = None
    preview_image: str = None
    video_url: str = None
