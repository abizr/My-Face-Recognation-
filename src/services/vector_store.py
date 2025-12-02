from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
import sqlalchemy as sa
from sqlalchemy.orm import Session
from loguru import logger

from src.config import Settings
from src.db import models


class VectorStore:
    def __init__(self, session: Session, settings: Settings):
        self.session = session
        self.settings = settings

    def upsert_person(self, name: str, email: Optional[str], labels: Optional[Dict[str, Any]]) -> models.Person:
        person = models.Person(name=name, email=email, labels=labels)
        self.session.add(person)
        self.session.commit()
        self.session.refresh(person)
        return person

    def insert_sample(
        self, person_id: UUID, image_uri: str, embedding: List[float], model_version: str, preproc_hash: str
    ) -> UUID:
        sample = models.FaceSample(
            id=uuid4(),
            person_id=person_id,
            image_uri=image_uri,
            embedding=embedding,
            model_version=model_version,
            preproc_hash=preproc_hash,
        )
        self.session.add(sample)
        self.session.commit()
        return sample.id

    def person_embeddings(self, person_id: UUID) -> List[List[float]]:
        stmt = sa.select(models.FaceSample.embedding).where(models.FaceSample.person_id == person_id)
        rows = self.session.execute(stmt).all()
        return [row[0] for row in rows]

    def knn_search(self, embedding: List[float], k: int = 5) -> List[Dict[str, Any]]:
        stmt = sa.text(
            """
            SELECT person_id, image_uri, embedding <=> :query_vec AS distance
            FROM face_samples
            ORDER BY embedding <-> :query_vec
            LIMIT :k;
            """
        )
        rows = self.session.execute(stmt, {"query_vec": embedding, "k": k}).all()
        return [
            {"person_id": row.person_id, "image_uri": row.image_uri, "score": 1.0 - row.distance}
            for row in rows
        ]
