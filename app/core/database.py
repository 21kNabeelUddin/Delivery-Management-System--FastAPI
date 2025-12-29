from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

SQLALCHAMY_DATABASE_URL = settings.DATABASE_URL

if SQLALCHAMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHAMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

__all__ = ["Base", "engine", "SessionLocal", "get_db"]

