# Face Recognition Service (PyTorch + FastAPI + pgvector + MinIO)

Production-style face recognition stack for enrollment, verification, and search. Uses PyTorch for embeddings, FastAPI for serving, PostgreSQL + pgvector for similarity search, and MinIO for object storage.

## Features
- Enroll faces with metadata, store originals in MinIO and embeddings in Postgres.
- Verify a claimed identity via cosine similarity thresholding.
- Identify/search via kNN over pgvector (HNSW index).
- Dataset management (list/delete/re-embed) and health/metrics endpoints.
- Model/version tracking for reproducibility.

## Quickstart
1. `python -m venv .venv && .\.venv\Scripts\activate`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill secrets/URLs.
4. `docker compose -f infra/docker-compose.yml up --build`
5. `uvicorn src.api.main:app --reload`
6. Open `http://localhost:8000/docs` for the API.

## Services
- API: FastAPI app exposing enroll/verify/search/health.
- DB: Postgres + pgvector extension for vector similarity.
- MinIO: S3-compatible storage for raw images.
- (Optional) Worker: background re-embedding or batch ingestion.

## Next Steps
- Swap the model checkpoint in `src/models/registry.py`.
- Add JWT auth in `src/services/auth.py`.
- Add liveness detection in `src/models/face_detector.py` or as a separate model.
- Wire CI (lint, mypy, pytest) and demo UI (Streamlit/React).
