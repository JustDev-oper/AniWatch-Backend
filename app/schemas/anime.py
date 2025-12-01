from datetime import datetime
from pydantic import BaseModel, HttpUrl


class Anime(BaseModel):
    id: int
    title: str
    description: str
    preview_image: HttpUrl
    video_url: HttpUrl
    created_at: datetime
    updated_at: datetime
    subtitle: str | None = None

    class Config:
        from_attributes = True


class AnimeCreate(BaseModel):
    title: str
    description: str
    video_url: HttpUrl
    subtitle: str | None = None
    preview_image: HttpUrl


class AnimeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    video_url: HttpUrl | None = None
    subtitle: str | None = None
    preview_image: HttpUrl | None = None
