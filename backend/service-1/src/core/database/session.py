from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.core.config import settings

engine_write = create_engine(
    settings.SQLALCHEMY_DATABASE_WRITE_URL,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"},
    pool_recycle=3600,
)
engine_read = create_engine(
    settings.SQLALCHEMY_DATABASE_READ_URL,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"},
    pool_recycle=3600,
)

session_local_write = sessionmaker(autocommit=False, autoflush=False, bind=engine_write)
session_local_read = sessionmaker(autocommit=False, autoflush=False, bind=engine_read)


class Base(DeclarativeBase):  # type: ignore[misc]
    """SQLAlchemy Declarative Base Class."""


def get_write_db() -> Generator[Session]:
    """Write DB Session."""
    db = session_local_write()
    try:
        yield db
    finally:
        db.close()


def get_read_db() -> Generator[Session]:
    """Read DB Session."""
    db = session_local_read()
    try:
        yield db
    finally:
        db.close()
