import io
import uuid
from datetime import timedelta
from typing import Optional
from minio import Minio
from minio.error import S3Error

from app.core.config import settings
from app.core.exceptions import StorageException
from app.core.logging import logger


class StorageRepository:
    def __init__(self):
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        """Verify object storage bucket exists, create if missing."""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created MinIO bucket: {self.bucket_name}")
        except Exception as e:
            logger.warning(f"Could not auto-verify MinIO bucket on init (will retry on upload): {str(e)}")

    def upload_bill_image(
        self,
        file_bytes: bytes,
        file_name: str,
        content_type: str,
        user_id: int,
        expense_id: int
    ) -> str:
        """
        Upload receipt image to MinIO and return ONLY the object key.
        Object key format: bills/user_{user_id}/expense_{expense_id}_{uuid}.{ext}
        """
        try:
            # Extract file extension
            ext = file_name.split(".")[-1] if "." in file_name else "jpg"
            object_key = f"bills/user_{user_id}/expense_{expense_id}_{uuid.uuid4().hex[:8]}.{ext}"

            # Prepare data stream
            data_stream = io.BytesIO(file_bytes)
            stream_length = len(file_bytes)

            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_key,
                data=data_stream,
                length=stream_length,
                content_type=content_type or "image/jpeg"
            )
            logger.info(f"Uploaded bill image to MinIO. Object Key: {object_key}")
            return object_key
        except Exception as e:
            logger.error(f"Failed to upload bill image to MinIO: {str(e)}")
            raise StorageException(f"Failed to upload bill image to storage: {str(e)}")

    def generate_presigned_url(self, object_key: str, expires_seconds: Optional[int] = None) -> Optional[str]:
        """
        Generate time-limited presigned GET URL for retrieving bill image.
        Replaces internal Docker endpoint (minio:9000) with external endpoint (localhost:9000) for client access.
        """
        if not object_key:
            return None

        expiry = timedelta(seconds=expires_seconds or settings.SIGNED_URL_EXPIRATION_SECONDS)
        try:
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_key,
                expires=expiry
            )

            # Replace internal Docker host name with external endpoint for browser/curl access
            if settings.MINIO_ENDPOINT != settings.MINIO_EXTERNAL_ENDPOINT:
                url = url.replace(settings.MINIO_ENDPOINT, settings.MINIO_EXTERNAL_ENDPOINT)

            return url
        except Exception as e:
            logger.error(f"Failed to generate presigned URL for key {object_key}: {str(e)}")
            return None

    def delete_bill_image(self, object_key: str) -> None:
        """Remove bill image object from MinIO storage."""
        if not object_key:
            return
        try:
            self.client.remove_object(self.bucket_name, object_key)
            logger.info(f"Deleted object {object_key} from MinIO")
        except Exception as e:
            logger.error(f"Failed to delete object {object_key} from MinIO: {str(e)}")
