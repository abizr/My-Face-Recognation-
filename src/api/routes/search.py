from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from src.api import schemas
from src.api.deps import get_embedder, get_settings_dep, get_vector_store
from src.models.inference import FaceEmbedder
from src.services.vector_store import VectorStore
from src.config import Settings

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=schemas.SearchResponse)
async def search(
    file: UploadFile = File(...),
    k: int = 5,
    embedder: FaceEmbedder = Depends(get_embedder),
    vectors: VectorStore = Depends(get_vector_store),
    settings: Settings = Depends(get_settings_dep),
):
    payload = await file.read()
    try:
        embedding = embedder.embed(payload).tolist()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    hits = vectors.knn_search(embedding=embedding, k=k)
    results: List[schemas.SearchResult] = [
        schemas.SearchResult(person_id=hit["person_id"], score=hit["score"], image_uri=hit["image_uri"])
        for hit in hits
    ]
    return schemas.SearchResponse(results=results, model_version=embedder.model_version)
