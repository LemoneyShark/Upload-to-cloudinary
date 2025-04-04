1. Install dependencies  

pip install -r requirements.txt

2. Create .env file :

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

3. Run server

Flask :
python Cloudinary_flask.py

FastAPI :
uvicorn Cloudinary_fastapi:app --reload