from fastapi import FastAPI, UploadFile, File
import uuid
import os
import json
from redis import Redis

# -------------------------
# App & Redis setup
# -------------------------
app = FastAPI()

redis_client = Redis(host="localhost", port=6379, db=0)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------
# Upload API
# -------------------------
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # unique job id
    job_id = str(uuid.uuid4())

    # save file
    file_path = os.path.join(UPLOAD_DIR, f"{job_id}_{file.filename}")
    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    # job data (ONLY metadata)
    job = {
        "job_id": job_id,
        "file_path": file_path,
        "filename": file.filename
    }

    # push job to redis
    try:
        redis_client.rpush("image_queue", json.dumps(job))
        redis_client.set(f"status:{job_id}", "queued")
    except Exception as e:
        return {
            "job_id": job_id,
            "status": "failed",
            "error": str(e)
        }

    return {
        "job_id": job_id,
        "status": "queued"
    }

# -------------------------
# Job status API
# -------------------------
@app.get("/status/{job_id}")
def check_status(job_id: str):
    status = redis_client.get(f"status:{job_id}")

    if not status:
        return {"error": "Invalid job id"}

    return {
        "job_id": job_id,
        "status": status.decode()
    }

# -------------------------
# Health check
# -------------------------
@app.get("/")
def root():
    return {"message": "Catalog Image Pipeline API running"}
