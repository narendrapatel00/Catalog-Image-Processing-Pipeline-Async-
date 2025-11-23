ss, thumbnail). Fast, scalable, and ideal for high-volume e-commerce workflows.
# 📦 Catalog Image Processing Pipeline (Async)

An asynchronous backend system that processes product images in the background using **FastAPI, Redis Queue (RQ), Pillow, and MongoDB**.  
It resizes, compresses, and optimizes images without slowing down the server, making it ideal for high-volume e-commerce platforms.

---

## 🚀 Features
- Upload product images via FastAPI
- Background processing using Redis Queue (RQ)
- Worker performs:
  - Resize
  - Compression
  - Thumbnail generation
- MongoDB stores job metadata and processed file details
- Check job status (pending, processing, completed)
- Download optimized images

---

## 🛠️ Tech Stack
- **FastAPI** – API backend  
- **Redis + Redis Queue** – Task queue for async processing  
- **Worker (Python)** – Background job handler  
- **Pillow (PIL)** – Image processing operations  
- **MongoDB** – Stores job data & metadata  

---

## 🔄 Architecture Flow

