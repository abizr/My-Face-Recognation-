from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, echo=settings.db_echo, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
