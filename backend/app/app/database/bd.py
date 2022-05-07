from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from typing import Generator

engine = create_engine(settings.DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_bd_session() -> Generator:
    try:
        bd = SessionLocal()
        yield bd
    finally:
        bd.close()