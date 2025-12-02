from fastapi import Depends
from sqlalchemy.orm import Session

from src.config import Settings, get_settings
from src.db.base import get_session
from src.models.inference import FaceEmbedder
from src.services.storage import Storage
from src.services.vector_store import VectorStore


def get_settings_dep() -> Settings:
    return get_settings()


def get_db(session: Session = Depends(get_session)) -> Session:
    return session


def get_storage(settings: Settings = Depends(get_settings_dep)) -> Storage:
    return Storage(settings)


_embedder = None


def get_embedder(settings: Settings = Depends(get_settings_dep)) -> FaceEmbedder:
    global _embedder
    if _embedder is None:
        _embedder = FaceEmbedder(settings)
    return _embedder


def get_vector_store(
    session: Session = Depends(get_db),
    settings: Settings = Depends(get_settings_dep),
) -> VectorStore:
    return VectorStore(session=session, settings=settings)
