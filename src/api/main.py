from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.config import get_settings
from src.db.base import engine
from src.db import models
from src.logging import setup_logging
from src.services.metrics import metrics_endpoint
from src.api.routes import enroll, verify, search, health, datasets


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Creating tables if missing.")
    models.Base.metadata.create_all(bind=engine)
    yield


settings = get_settings()
app = FastAPI(title="Face Recognition Service", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(enroll.router)
app.include_router(verify.router)
app.include_router(search.router)
app.include_router(datasets.router)
app.include_router(health.router)


@app.get("/metrics")
def metrics():
    return metrics_endpoint()
