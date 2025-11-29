from fastapi import APIRouter, HTTPException
from app.db import jobs_collection

router = APIRouter(tags=["status"])

@router.get("/status/{job_id}")
def get_status(job_id: str):
    job = jobs_collection.find_one({"job_id": job_id}, {"_id": 0})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job
