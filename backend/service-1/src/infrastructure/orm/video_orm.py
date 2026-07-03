"""service-1: SQLAlchemy Video ORM Model.

Infrastructure 계층 전용. Domain 계층으로 노출하지 않는다.
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.database import Base


class VideoORM(Base):
    """videos 테이블 ORM 매핑."""

    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(Text)
    url = Column(String)
    thumbnail = Column(String, nullable=True)
    analysis_status = Column(String, default="pending")
    ai_summary = Column(Text, nullable=True)
    ai_audio = Column(String, nullable=True)
    is_ai_thumbnail = Column(Boolean, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserORM", back_populates="videos")
