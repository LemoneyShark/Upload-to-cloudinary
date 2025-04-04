
import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

load_dotenv()

app = FastAPI()

# ✅ กำหนด CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔥 ระวัง: Production ควรกำหนด Origin ให้ปลอดภัยขึ้น
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ตั้งค่า Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/gif", "video/mp4"}
MAX_FILE_SIZE_MB = 10 * 1024 * 1024  # 10MB


class UploadLinkRequest(BaseModel):
    url: str


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Cloudinary Uploader"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # ✅ เช็ค MIME Type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="File type not allowed")

    # ✅ เช็คขนาดไฟล์

    
    # ✅ อัปโหลดไปที่ Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(file.file, resource_type="auto")
        return {"message": "Cloudinary successful!", "cloudinaryUrl": upload_result["secure_url"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.post("/upload_link")
async def upload_link(data: UploadLinkRequest):
    # ✅ อัปโหลดไฟล์จาก URL ไปที่ Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(data.url, resource_type="auto")
        return {"message": "Cloudinary successful!", "cloudinaryUrl": upload_result["secure_url"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
