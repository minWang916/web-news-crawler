import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@links.qyv15f1.mongodb.net/?retryWrites=true&w=majority&appName=Links"

if (MONGO_URI is None):
  MONGO_USERNAME = os.getenv("MONGO_USER_NAME")
  MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
  MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@links.qyv15f1.mongodb.net/?retryWrites=true&w=majority&appName=Links"
