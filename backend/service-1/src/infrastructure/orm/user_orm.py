"""service-1: SQLAlchemy User ORM Model."""

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from src.core.database import Base


class UserORM(Base):
    """users 테이블 ORM 매핑."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    videos = relationship("VideoORM", back_populates="owner")
