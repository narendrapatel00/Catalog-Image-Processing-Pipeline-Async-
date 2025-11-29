import shutil
from uuid import uuid4
from pathlib import Path
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from redis import Redis
from rq import Queue

from app.config import get_settings
from app.db import jobs_collection
from app.workers.image_worker import process_image_job

router = APIRouter(tags=["upload"])
settings = get_settings()

redis_conn = Redis.from_url(settings.REDIS_URL)
queue = Queue("default", connection=redis_conn)

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only images allowed.")

    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(file.filename).suffix or ".jpg"
    filename = f"{uuid4().hex}{suffix}"
    saved_path = upload_dir / filename

    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job_id = uuid4().hex
    jobs_collection.insert_one({
        "job_id": job_id,
        "status": "queued",
        "original_image_path": str(saved_path),
        "created_at": datetime.utcnow()
    })

    queue.enqueue(process_image_job, job_id, str(saved_path))

    return {"job_id": job_id, "message": "Image uploaded & queued"}
