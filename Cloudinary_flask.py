import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

#Extra
from flask_cors import CORS  # CORS
#from flask_talisman import Talisman  # Security Headers

app = Flask(__name__)
load_dotenv()

CORS(app)  # Open request API all domain
#Talisman(app)  # Protect XSS & Clickjacking

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

#no part
@app.route("/")
def index():
    return render_template("index.html")

#paht upload
@app.route("/upload", methods=["POST"])
def upload_file():

    file = request.files.get("file")#Recieve form form-data
    if not file:
        return jsonify({"error": "No file uploaded"}), 400


    # Chaek file size (10MB)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > 10 * 1024 * 1024:
        return jsonify({"error": "File is over 10MB"}), 400

    # upload to cloudinary 
    try:
        upload_result = cloudinary.uploader.upload(file, resource_type="auto")
        return jsonify({
            "message": "Cloudinary successful!",
            "cloudinaryUrl": upload_result["secure_url"]
        }), 200
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500


#paht upload_link
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
    app.run(port=5000, debug=os.getenv("DEBUG", "False") == "True")
