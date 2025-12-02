import numpy as np
from uuid import UUID
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from src.api import schemas
from src.api.deps import get_embedder, get_settings_dep, get_vector_store
from src.models.inference import FaceEmbedder
from src.services.vector_store import VectorStore
from src.config import Settings

router = APIRouter(prefix="/verify", tags=["verify"])


@router.post("/{person_id}", response_model=schemas.VerifyResponse)
async def verify(
    person_id: UUID,
    file: UploadFile = File(...),
    embedder: FaceEmbedder = Depends(get_embedder),
    vectors: VectorStore = Depends(get_vector_store),
    settings: Settings = Depends(get_settings_dep),
):
    payload = await file.read()
    try:
        probe = embedder.embed(payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    refs = vectors.person_embeddings(person_id)
    if not refs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found or no samples")

    ref_matrix = np.stack(refs)
    probe_norm = probe / np.linalg.norm(probe)
    ref_norm = ref_matrix / np.linalg.norm(ref_matrix, axis=1, keepdims=True)
    scores = ref_norm @ probe_norm
    best = float(scores.max())
    return schemas.VerifyResponse(
        match=best >= settings.verify_threshold,
        score=best,
        threshold=settings.verify_threshold,
        model_version=embedder.model_version,
    )
