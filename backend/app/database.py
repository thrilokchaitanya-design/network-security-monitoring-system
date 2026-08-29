import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    sessionmaker,
)


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


# ============================================================
# Database engine
# ============================================================

engine = create_engine(
    DATABASE_URL
)


# ============================================================
# SQLAlchemy Base
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# Database session
# ============================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()