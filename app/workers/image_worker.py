from datetime import datetime
from pathlib import Path
from app.config import get_settings
from app.db import jobs_collection
from app.utils.image_processing import process_image

settings = get_settings()

def process_image_job(job_id: str, original_image_path: str):
    try:
        jobs_collection.update_one({"job_id": job_id}, {"$set": {"status": "processing"}})

        input_path = Path(original_image_path)
        output_path = Path(settings.PROCESSED_DIR) / input_path.name

        meta = process_image(str(input_path), str(output_path))

        size_before = input_path.stat().st_size
        size_after = output_path.stat().st_size

        jobs_collection.update_one(
            {"job_id": job_id},
            {"$set": {
                "status": "completed",
                "completed_at": datetime.utcnow(),
                "processed_image_path": str(output_path),
                "size_before": size_before,
                "size_after": size_after,
                **meta
            }}
        )
    except Exception as e:
        jobs_collection.update_one(
            {"job_id": job_id},
            {"$set": {"status": "failed", "error": str(e)}}
        )
