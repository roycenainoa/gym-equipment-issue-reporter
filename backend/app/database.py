"""Database setup: SQLAlchemy engine, session factory, and the FastAPI dependency.

A single SQLite file (gym.db) provides persistent relational storage, satisfying
the Reliability requirement (data survives server restarts).
"""
from collections.abc import Generator
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# The database file lives next to the backend by default; override with DATABASE_URL
# (e.g. inside Docker) without changing code.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gym.db")

# check_same_thread=False is required for SQLite when used by FastAPI's worker threads.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and guarantee it is closed after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
