from pymongo import MongoClient
import os

# You can store this in an environment variable later
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "ocr_llm_system"
COLLECTION_NAME = "documents"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_document(data: dict):
    """Insert a document into the MongoDB collection."""
    result = collection.insert_one(data)
    return str(result.inserted_id)
