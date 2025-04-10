from fastapi import FastAPI
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load .env variables into the environment
load_dotenv()

# Read MongoDB configuration from environment variables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Create a MongoDB client and connect to the specified database and collection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Initialize the FastAPI app
app = FastAPI()

# Define an API route at /sensors that responds to GET requests
@app.get("/sensors")
def get_sensors():
    """Return the 10 most recent sensor entries."""
    # Query MongoDB for the 10 most recent documents, sorted by timestamp (ts) descending
    cursor = collection.find().sort("ts", -1).limit(10)

    # Prepare the response list
    results = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])  # Convert MongoDB ObjectId to string for JSON serialization
        results.append(doc)

    # Return the list of documents as JSON
    return results
