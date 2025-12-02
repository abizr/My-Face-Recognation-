from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.deps import get_db, get_embedder, get_vector_store
from src.db import models
from src.models.inference import FaceEmbedder
from src.services.vector_store import VectorStore

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.get("/persons")
def list_persons(db: Session = Depends(get_db)):
    stmt = select(models.Person)
    rows = db.execute(stmt).scalars().all()
    return [{"id": p.id, "name": p.name, "email": p.email, "labels": p.labels} for p in rows]


@router.get("/persons/{person_id}/samples")
def list_samples(person_id: UUID, db: Session = Depends(get_db)):
    stmt = select(models.FaceSample).where(models.FaceSample.person_id == person_id)
    rows = db.execute(stmt).scalars().all()
    return [
        {
            "id": s.id,
            "image_uri": s.image_uri,
            "model_version": s.model_version,
            "preproc_hash": s.preproc_hash,
            "created_at": s.created_at,
        }
        for s in rows
    ]


@router.post("/reembed/{person_id}")
async def reembed_person(
    person_id: UUID,
    vectors: VectorStore = Depends(get_vector_store),
    embedder: FaceEmbedder = Depends(get_embedder),
):
    # Placeholder: in real system pull original images from MinIO and recompute.
    existing = vectors.person_embeddings(person_id)
    if not existing:
        raise HTTPException(status_code=404, detail="No samples to re-embed")
    return {"person_id": person_id, "status": "queued", "target_model": embedder.model_version}
