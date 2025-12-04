import os, uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pymongo import MongoClient
from redis import Redis
from PIL import Image, ImageOps

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

DATA_DIR = "./data"
UPLOAD_DIR = DATA_DIR + "/uploads"
PROCESSED_DIR = DATA_DIR + "/processed"
THUMB_DIR = DATA_DIR + "/thumbs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(THUMB_DIR, exist_ok=True)

client = MongoClient(MONGO_URL)
db = client["catalog_pipeline"]
images = db["images"]

redis_conn = Redis.from_url(REDIS_URL)

app = FastAPI(title="Catalog Image Pipeline")

def optimize_image(input_path, output_path):
    from PIL import Image
    with Image.open(input_path) as im:
        if im.mode != "RGB":
            im = im.convert("RGB")
        w, h = im.size
        if w > 1024:
            h_new = int((1024 / w) * h)
            im = im.resize((1024, h_new))
        im.save(output_path, "JPEG", quality=85)

def make_thumb(input_path, output_path):
    with Image.open(input_path) as im:
        im = ImageOps.fit(im, (200, 200))
        im.save(output_path, "JPEG", quality=80)

def process_image(job_id, original, filename):
    print("⚡ Processing:", job_id)
    images.update_one({"job_id": job_id}, {"$set": {"status": "processing"}})

    out = f"{PROCESSED_DIR}/{job_id}_optimized.jpg"
    th = f"{THUMB_DIR}/{job_id}_thumb.jpg"

    try:
        optimize_image(original, out)
        make_thumb(original, th)

        images.update_one(
            {"job_id": job_id},
            {"$set": {
                "status": "done",
                "optimized": out,
                "thumb": th,
            }}
        )
        print("✅ DONE:", job_id)
    except Exception as e:
        print("❌ ERROR:", e)
        images.update_one(
            {"job_id": job_id},
            {"$set": {"status": "failed", "error": str(e)}}
        )

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if "image" not in file.content_type:
        raise HTTPException(400, "Only images allowed")

    job_id = str(uuid.uuid4())
    filename = job_id + "_" + file.filename
    path = f"{UPLOAD_DIR}/{filename}"

    data = await file.read()
    with open(path, "wb") as f:
        f.write(data)

    images.insert_one({
        "job_id": job_id,
        "filename": filename,
        "status": "queued",
        "original": path,
    })

    redis_conn.rpush("job_queue", f"{job_id}|{path}|{filename}")

    return {"job_id": job_id}

@app.get("/status/{job_id}")
def status(job_id: str):
    doc = images.find_one({"job_id": job_id}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "Not found")
    return doc

@app.get("/download/{job_id}/{kind}")
def download(job_id: str, kind: str):
    doc = images.find_one({"job_id": job_id})
    if not doc:
        raise HTTPException(404, "Not found")

    path = doc.get("optimized") if kind == "optimized" else doc.get("thumb")

    if not path or not os.path.exists(path):
        raise HTTPException(404, "Not ready")

    return FileResponse(path)
