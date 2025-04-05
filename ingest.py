import os
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from validate import validate_record
from dotenv import load_dotenv
import logging

# Load environment variables from .env
load_dotenv()

# Setup logging
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "invalid_rows.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    filemode="w",
    level=logging.WARNING,
    format="%(asctime)s - Row %(row)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "environment")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "sensor_data")
BATCH_SIZE = 1000

def load_csv():
    # Load CSV
    try:
        df = pd.read_csv("iot_telemetry_data.csv")
        print(f"Loaded {len(df)} records from CSV.")
        return df
    except Exception as e:
        print(f"Error reading CSV: {e}")
        exit(1)

def insert_data(valid_records, collection):
    # Insert into MongoDB in batches
    print(f"Ingesting {len(valid_records)} valid records into MongoDB...")

    for i in range(0, len(valid_records), BATCH_SIZE):
        batch = valid_records[i:i + BATCH_SIZE]
        try:
            collection.insert_many(batch)
            print(f"Inserted batch {i // BATCH_SIZE + 1}")
        except BulkWriteError as bwe:
            print(f"Bulk write error: {bwe.details}")
            
def val_and_prep(df):
    # Validate and prepare records
    valid_records = []
    invalid_count = 0

    for idx, row in df.iterrows():
        try:
            record = validate_record(row.to_dict())
            valid_records.append(record)
        except Exception as e:
            invalid_count += 1
            logging.warning(str(e), extra={"row": idx})
    
    return valid_records, invalid_count

def main():    
    # MongoDB connection
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Load CSV
    df = load_csv()

    # Validate and prepare records
    valid_records, invalid_count = val_and_prep(df)

    # Insert into MongoDB in batches
    insert_data(valid_records, collection)

    print("Ingestion complete.")
    print(f"Valid rows inserted: {len(valid_records)}")
    print(f"Invalid rows skipped: {invalid_count}")
    print(f"Invalid rows logged in: {LOG_FILE}")
    
if __name__ == "__main__":
    main()
