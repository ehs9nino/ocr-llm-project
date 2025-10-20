# db.py
import os
import certifi
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

# --- Config ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "ocr_llm_system")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")


def get_client(uri: str):
    """Return a MongoClient with certifi CA (for Atlas & local)"""
    return MongoClient(
        uri,
        serverSelectionTimeoutMS=8000,
        tlsCAFile=certifi.where() if "mongodb+srv" in uri else None,
    )


# --- Initialize client safely ---
try:
    client = get_client(MONGO_URI)
    client.admin.command("ping")
    print(f"[✅] Connected to MongoDB at {MONGO_URI}")
except Exception as e:
    print(f"[⚠️] Failed to connect to Atlas ({e}), trying local MongoDB...")
    try:
        client = get_client("mongodb://localhost:27017")
        client.admin.command("ping")
        print("[✅] Connected to local MongoDB")
    except Exception as e2:
        print(f"[❌] Could not connect to any MongoDB: {e2}")
        client = None

# --- Get collection handle ---
if client:
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
else:
    db = None
    collection = None


def save_document(data: dict):
    """Insert document into MongoDB (safe insert)"""
    if not collection:
        print("⚠️ MongoDB not connected — cannot insert.")
        return None
    try:
        result = collection.insert_one(data)
        print(f"✅ Inserted document with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        print(f"❌ MongoDB insert failed: {e}")
        return None


def ping():
    """Quick connection test"""
    if not client:
        return {"status": "disconnected"}
    try:
        client.admin.command("ping")
        return {"status": "ok"}
    except ServerSelectionTimeoutError as e:
        return {"status": "error", "message": str(e)}
