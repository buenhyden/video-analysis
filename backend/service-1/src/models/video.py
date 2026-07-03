from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(Text)
    url = Column(String)
    thumbnail = Column(String, nullable=True)

    # status: pending, processing, completed, failed
    analysis_status = Column(String, default="pending")
    # AI가 생성한 요약본
    ai_summary = Column(Text)
    ai_audio = Column(String, nullable=True)

    is_ai_thumbnail = Column(Boolean, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="videos")
