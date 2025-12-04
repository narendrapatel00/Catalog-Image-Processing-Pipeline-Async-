import time
from redis import Redis
from app import process_image
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

def run_worker():
    print("⚡ Windows Manual Worker Started... (NO RQ, NO FORK)")
    redis_conn = Redis.from_url(REDIS_URL)

    while True:
        job = redis_conn.blpop("job_queue", timeout=5)
        if job:
            _, payload = job
            payload = payload.decode()
            print("📥 Job Received:", payload)

            try:
                job_id, path, filename = payload.split("|")
                process_image(job_id, path, filename)
                print("✅ Job Done:", job_id)
            except Exception as e:
                print("❌ Error:", e)
        else:
            time.sleep(1)

if __name__ == "__main__":
    run_worker()
