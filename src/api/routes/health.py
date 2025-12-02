import sqlalchemy as sa
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api import schemas
from src.api.deps import get_db, get_embedder, get_settings_dep, get_storage
from src.models.inference import FaceEmbedder
from src.services.storage import Storage
from src.config import Settings

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def liveness():
    return {"status": "ok"}


@router.get("/ready", response_model=schemas.HealthStatus)
def readiness(
    db: Session = Depends(get_db),
    storage: Storage = Depends(get_storage),
    embedder: FaceEmbedder = Depends(get_embedder),
    settings: Settings = Depends(get_settings_dep),
):
    db_status = "ok"
    try:
        db.execute(sa.text("SELECT 1"))
    except Exception:
        db_status = "error"

    storage_status = "ok" if storage.client.bucket_exists(settings.minio_bucket) else "error"
    overall = "ok" if db_status == "ok" and storage_status == "ok" else "degraded"
    return schemas.HealthStatus(status=overall, db=db_status, storage=storage_status, model_version=embedder.model_version)
