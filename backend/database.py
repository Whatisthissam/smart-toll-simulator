import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Setup MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "smart_toll_simulator")

# Simple singleton connection to keep it beginner friendly
try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    print(f"Connected to MongoDB database: {DB_NAME}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None

def get_db():
    return db
