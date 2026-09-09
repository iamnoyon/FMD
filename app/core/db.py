from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# DB URL
DB_URL = 'postgresql://neondb_owner:npg_aqNj3ZfOKkB7@ep-rapid-queen-aecqqwut-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'


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



