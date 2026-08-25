from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# DB URL
DB_URL = 'postgresql+psycopg://postgres:674@localhost:5432/fresh_milk'


engine = create_engine(DB_URL)
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



