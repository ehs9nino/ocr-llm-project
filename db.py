from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Mongo config
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "ocr_llm_system"
COLLECTION_NAME = "documents"

# Connect

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=10000
)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_document(data: dict):
    """Insert a document into the MongoDB collection."""
    try:
        print(f"📤 Inserting into MongoDB: {data}")
        result = collection.insert_one(data)
        print(f"✅ Inserted with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        print(f"❌ MongoDB insert failed: {e}")
        return None
