from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        protected_namespaces=("settings_",),
    )

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    env: str = "local"

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/frdb"
    db_echo: bool = False
    pgvector_dim: int = 512

    minio_endpoint: str = "localhost:9000"
    minio_bucket: str = "faces"
    minio_secure: bool = False
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"

    model_path: str = "./models/arcface_resnet50.pth"
    model_version: str = "arcface-resnet50-v1"
    preproc_hash: str = "basic-rsz112-norm05"
    verify_threshold: float = 0.55

    jwt_secret: str = "devsecret"
    jwt_alg: str = "HS256"
    allowed_origins: List[str] = ["*"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
