import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Index, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from pgvector.sqlalchemy import Vector

from src.config import get_settings

Base = declarative_base()
settings = get_settings()


class Person(Base):
    __tablename__ = "persons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    labels = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    samples = relationship("FaceSample", back_populates="person", cascade="all, delete-orphan")


class FaceSample(Base):
    __tablename__ = "face_samples"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    image_uri = Column(Text, nullable=False)
    embedding = Column(Vector(settings.pgvector_dim), nullable=False)
    model_version = Column(String(128), nullable=False)
    preproc_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    person = relationship("Person", back_populates="samples")


Index(
    "idx_face_samples_embedding_hnsw",
    FaceSample.embedding,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding": "vector_cosine_ops"},
)
