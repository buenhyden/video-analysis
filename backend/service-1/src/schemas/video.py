from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VideoBase(BaseModel):
    title: str
    category: str
    description: str
    url: str
    thumbnail: str | None = None


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    id: int
    owner_id: int
    created_at: datetime

    # 추가된 필드
    analysis_status: str
    ai_summary: str | None = None

    model_config = ConfigDict(from_attributes=True)
