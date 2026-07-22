from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Personal Expense Tracker API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # JWT Settings
    SECRET_KEY: str = "super-secret-jwt-key-change-this-in-production-use-openssl-rand-hex-32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # PostgreSQL Database Settings
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "expense_user"
    POSTGRES_PASSWORD: str = "expense_password"
    POSTGRES_DB: str = "expense_tracker_db"
    DATABASE_URL: Union[str, None] = None

    @field_validator("DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: Union[str, None], info) -> str:
        if isinstance(v, str) and v.strip():
            return v
        values = info.data
        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        server = values.get("POSTGRES_SERVER")
        port = values.get("POSTGRES_PORT")
        db = values.get("POSTGRES_DB")
        return f"postgresql://{user}:{password}@{server}:{port}/{db}"

    # MinIO Settings
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_EXTERNAL_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "expense-bills"
    MINIO_SECURE: bool = False

    # Signed URL expiry in seconds (default 1 hour = 3600 seconds)
    SIGNED_URL_EXPIRATION_SECONDS: int = 3600

    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:8000", "http://localhost:3000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
