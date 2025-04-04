import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

#Extra
from flask_cors import CORS  # CORS
from flask_talisman import Talisman  # Security Headers

app = Flask(__name__)
load_dotenv()

CORS(app)  # Open request API all domain
Talisman(app)  # Protect XSS & Clickjacking

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file") #  Recieve form form-data
    # เช็คขนาดไฟล์ (10MB)
    if file.content_length and file.content_length > 10 * 1024 * 1024:
        return jsonify({"error": "File is over 10MB"}), 400
    
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    upload_result = cloudinary.uploader.upload(file, resource_type="auto")  # Upload to Cloudinary
    return jsonify({
        "message": "Cloudinary successful!",
        "cloudinaryUrl": upload_result["secure_url"]
    }), 200


# ✅ อัปโหลดจากลิงก์
@app.route("/upload_link", methods=["POST"])
def upload_link():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data["url"]

    try:
        upload_result = cloudinary.uploader.upload(url, resource_type="auto")
        return jsonify({
            "message": "Cloudinary successful!",
            "cloudinaryUrl": upload_result["secure_url"]
        }), 200
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500
    

if __name__ == "__main__":
    app.run(port=5000, debug=True)
