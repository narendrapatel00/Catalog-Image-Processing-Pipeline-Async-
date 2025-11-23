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

User → FastAPI Upload API
→ Redis Queue (Job Added)
→ Worker (Pillow Processing)
→ MongoDB (Store Output)
→ User checks Status / Downloads File

yaml
Copy code

---

## 📁 Project Structure (Example)

Catalog-Image-Processing-Pipeline-Async/
│── app/
│ ├── main.py
│ ├── api/
│ │ ├── upload.py
│ │ ├── status.py
│ │ └── download.py
│ ├── workers/
│ │ └── image_worker.py
│ ├── utils/
│ │ └── image_processing.py
│── processed/
│── uploads/
│── requirements.txt
│── README.md

yaml
Copy code

---

## 📝 API Endpoints

### **1. Upload Image**
POST /upload

markdown
Copy code

### **2. Get Job Status**
GET /status/{job_id}

markdown
Copy code

### **3. Download Processed Image**
GET /download/{job_id}

yaml
Copy code

---

## 🧪 How it Works (Demo Summary)

1. User uploads an image  
2. FastAPI saves it and sends a job to Redis Queue  
3. Background worker picks the job  
4. Pillow processes the image (resize, compress, thumbnail)  
5. Final image & metadata saved in MongoDB  
6. User checks status & downloads processed image

---

## 📷 Demo (Explanation for GitHub)

### **Step 1: Upload an Image**
User sends a POST request with the image to `/upload`.

### **Step 2: Job Queued**
FastAPI pushes the job to Redis Queue and returns a `job_id`.

### **Step 3: Background Processing**
Worker retrieves job → processes image → saves result.

### **Step 4: Check Job Status**
User polls `/status/{job_id}`.

### **Step 5: Download Final Image**
Once completed, user downloads optimized image from `/download/{job_id}`.

---

## 📌 Status
🔨 Development in progress  
📅 Architecture, PRD, schema & setup completed  
🚀 APIs & worker integration coming next

---

## 👨‍💻 Author
**Narendra Patel**  
2nd Year AIML — Polaris School of Technology
⭐ 📸 Project Demo (Short & Sweet for GitHub or Mentor)
Demo Steps:

1️⃣ User uploads a product image
→ FastAPI accepts it and stores the file.

2️⃣ Job enters Redis Queue
→ Fast, temporary storage for background tasks.

3️⃣ Worker picks the job
→ Runs Pillow functions:

Resize

Compress

Optimize

Thumbnail

4️⃣ MongoDB stores final results
→ Processed file path + metadata + timings.

5️⃣ User checks status
→ Gets "pending / processing / completed".

6️⃣ User downloads processed image
→ Optimized, smaller, catalog-ready image.
