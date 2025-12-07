import time
import json
import os
from redis import Redis
from PIL import Image

# -------------------------
# Redis setup
# -------------------------
redis_client = Redis(host="localhost", port=6379, db=0)

PROCESSED_DIR = "processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("⚡ Windows Manual Worker Started")
print("Waiting for jobs...")

while True:
    try:
        # blocking pop (waits for job)
        _, job_data = redis_client.blpop("image_queue")

        job = json.loads(job_data)
        job_id = job["job_id"]
        file_path = job["file_path"]
        filename = job["filename"]

        # update status
        redis_client.set(f"status:{job_id}", "processing")
        print(f"🔧 Processing job: {job_id}")

        # image processing
        img = Image.open(file_path)
        img = img.resize((800, 800))

        output_path = os.path.join(PROCESSED_DIR, filename)
        img.save(output_path, optimize=True, quality=80)

        # mark completed
        redis_client.set(f"status:{job_id}", "completed")
        print(f"✅ Completed job: {job_id}")

    except Exception as e:
        redis_client.set(f"status:{job_id}", "failed")
        print("❌ Job failed:", str(e))

    time.sleep(1)
