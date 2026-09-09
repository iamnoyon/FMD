from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DB_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)

localSession = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = localSession()
    try:
        yield db
    finally:
        db.close()