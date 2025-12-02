import json
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from src.api import schemas
from src.api.deps import get_embedder, get_settings_dep, get_storage, get_vector_store
from src.models.inference import FaceEmbedder
from src.services.storage import Storage
from src.services.vector_store import VectorStore
from src.config import Settings

router = APIRouter(prefix="/enroll", tags=["enroll"])


@router.post("", response_model=schemas.EnrollResponse)
async def enroll(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: Optional[str] = Form(None),
    labels: Optional[str] = Form(None),
    embedder: FaceEmbedder = Depends(get_embedder),
    storage: Storage = Depends(get_storage),
    vectors: VectorStore = Depends(get_vector_store),
    settings: Settings = Depends(get_settings_dep),
):
    payload = await file.read()
    try:
        embedding = embedder.embed(payload).tolist()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    label_dict = json.loads(labels) if labels else None
    person = vectors.upsert_person(name=name, email=email, labels=label_dict)
    key = storage.save_bytes(payload)
    sample_id = vectors.insert_sample(
        person_id=person.id,
        image_uri=key,
        embedding=embedding,
        model_version=embedder.model_version,
        preproc_hash=embedder.preproc_hash,
    )
    return schemas.EnrollResponse(
        person_id=person.id,
        sample_id=sample_id,
        embedding_dim=len(embedding),
        model_version=embedder.model_version,
    )
