import io
from typing import Optional
from uuid import uuid4
from minio import Minio
from minio.error import S3Error
from loguru import logger

from src.config import Settings


class Storage:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        self.ensure_bucket()

    def ensure_bucket(self) -> None:
        if not self.client.bucket_exists(self.settings.minio_bucket):
            self.client.make_bucket(self.settings.minio_bucket)
            logger.info(f"Created bucket {self.settings.minio_bucket}")

    def save_bytes(self, data: bytes, suffix: str = ".jpg") -> str:
        key = f"faces/{uuid4()}{suffix}"
        self.client.put_object(
            self.settings.minio_bucket,
            key,
            io.BytesIO(data),
            length=len(data),
            content_type="image/jpeg",
        )
        return key

    def presign(self, key: str, expires: int = 3600) -> Optional[str]:
        try:
            return self.client.presigned_get_object(self.settings.minio_bucket, key, expires=expires)
        except S3Error as e:
            logger.error(f"Presign failed: {e}")
            return None
