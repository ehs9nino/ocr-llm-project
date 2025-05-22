import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Get URI
MONGO_URI = os.getenv("MONGO_URI")
print(f"Connecting to MongoDB: {MONGO_URI}")

# Connect to Atlas
client = MongoClient(MONGO_URI, tls=True)
db = client["ocr_llm_system"]
print("✅ Connected!")

# Show collections
print("Collections:", db.list_collection_names())
