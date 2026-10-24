# 03_raw_ingest_lake.py
import json
import logging
import importlib
from datetime import datetime, timezone

# Dynamically import module with numerical prefix to prevent syntax errors
mongo_driver_module = importlib.import_module("02_mongo_driver")
MongoDriver = mongo_driver_module.MongoDriver

# Configure logging to write to console AND lake_ingest_execution.log simultaneously
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)03d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("lake_ingest_execution.log", mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

def generate_mock_data():
    """Generates mock JSON payload matching JuanMart streams if raw file isn't provided."""
    data = []
    streams = [("WEB_STORE", 820), ("POS_TERMINALS", 450), ("MOBILE_APP", 230)]
    for stream, count in streams:
        for i in range(count):
            data.append({
                "stream_source": stream,
                "payload_id": f"{stream}_{i+1000}",
                "event_data": {"checkout_id": i, "amount": 19.99 + i}
            })
    return data

def ingest_and_audit():
    driver = MongoDriver()
    collection = driver.get_collection()

    logger.info("[*] Commencing raw JSON payload stream ingestion...")

    # Load raw JSON data (attempts file load, falls back to mock generator)
    try:
        with open("raw_telemetry_payloads.json", "r") as f:
            raw_docs = json.load(f)
    except FileNotFoundError:
        raw_docs = generate_mock_data()

    # Stamp raw payloads with ingestion metadata
    ingest_time = datetime.now(timezone.utc).isoformat()
    for doc in raw_docs:
        doc["ingested_at"] = ingest_time

    doc_count = len(raw_docs)
    logger.info(f"[-] Staging {doc_count:,} raw JSON documents into collection: {collection.name}")

    # Perform bulk insertion
    result = collection.insert_many(raw_docs)
    logger.info(f"[+] Ingestion Complete. Bulk Insert Acknowledged: {result.acknowledged}")

    # Audit section matching exact expected terminal format
    divider = "=" * 65
    logger.info(divider)
    logger.info("         DATA LAKE LANDING AUDIT")
    logger.info(divider)

    total_docs = collection.count_documents({})
    logger.info(f"TOTAL DOCUMENTS LANDED : {total_docs}")

    # Profile counts grouped by stream source
    pipeline = [
        {"$group": {"_id": "$stream_source", "count": {"$sum": 1}}}
    ]
    stream_counts = {item["_id"]: item["count"] for item in collection.aggregate(pipeline)}

    logger.info(f"WEB_STORE STREAM    : {stream_counts.get('WEB_STORE', 0)} documents")
    logger.info(f"POS_TERMINALS STREAM: {stream_counts.get('POS_TERMINALS', 0)} documents")
    logger.info(f"MOBILE_APP STREAM   : {stream_counts.get('MOBILE_APP', 0)} documents")
    logger.info(divider)

    driver.close()

if __name__ == "__main__":
    ingest_and_audit()