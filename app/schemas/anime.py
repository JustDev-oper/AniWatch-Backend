from datetime import datetime
from pydantic import BaseModel, HttpUrl


class Anime(BaseModel):
    id: int
    title: str
    subtitle: str | None = None
    description: str
    preview_image: HttpUrl
    video_url: HttpUrl
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnimeCreate(BaseModel):
    title: str
    subtitle: str | None = None
    description: str
    preview_image: HttpUrl
    video_url: HttpUrl


class AnimeUpdate(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    description: str | None = None
    preview_image: HttpUrl | None = None
    video_url: HttpUrl | None = None