from pydantic import BaseSettings
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "catalog_image_pipeline"
    MONGO_JOBS_COLLECTION: str = "jobs"

    REDIS_URL: str = "redis://localhost:6379/0"

    UPLOAD_DIR: str = str(BASE_DIR / "uploads")
    PROCESSED_DIR: str = str(BASE_DIR / "processed")

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
