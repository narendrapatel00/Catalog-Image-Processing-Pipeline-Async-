from fastapi import FastAPI
from app.api import upload, status as status_api, download

app = FastAPI(title="Catalog Image Processing Pipeline (Async)", version="1.0.0")

app.include_router(upload.router, prefix="/api")
app.include_router(status_api.router, prefix="/api")
app.include_router(download.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Catalog Image Processing Pipeline is running!"}
