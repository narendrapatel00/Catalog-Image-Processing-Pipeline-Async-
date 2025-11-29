from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.db import jobs_collection

router = APIRouter(tags=["download"])

@router.get("/download/{job_id}")
def download_processed(job_id: str):
    job = jobs_collection.find_one({"job_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")

    if job.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Job not completed yet.")

    processed_path = job.get("processed_image_path")
    if not processed_path or not Path(processed_path).exists():
        raise HTTPException(status_code=500, detail="Processed image missing.")

    return FileResponse(processed_path, media_type="image/jpeg")
