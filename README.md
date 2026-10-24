# Real-Time MongoDB Data Lake Ingestion & Stream Profiling

## 📌 Overview
An enterprise data lake landing pipeline engineered to ingest multi-channel telemetry streams (Web Store, POS Terminals, and Mobile App payloads) into MongoDB. The system dynamically manages database driver connections via `.env` configurations, stamps ISO-8601 ingestion metadata onto landed JSON documents, and executes MongoDB aggregation pipelines to audit stream integrity and volume distribution.

## 🛠 Tech Stack
* **Database & NoSQL Storage:** MongoDB, Mongo Shell (`01_datalake_setup.mongodb.js`)
* **Language & Drivers:** Python 3.x, `pymongo`, `python-dotenv`
* **Data Processing & Audit:** MongoDB Aggregation Framework (`$group`, `$sum`)
* **Logging:** Dual Stream/File Execution Handler (`lake_ingest_execution.log`)

## ⚡ Core Pipeline Architecture

```text
 ┌───────────────────────────────────┐
 │ Telemetry Streams                 │
 │ (WEB_STORE, POS, MOBILE_APP)      │
 └─────────────────┬─────────────────┘
                   │
                   ▼
 ┌───────────────────────────────────┐
 │ Python Ingestion Orchestrator     │
 │ - Stamps ISO-8601 ingested_at     │
 │ - Bulk insert into MongoDB        │
 └─────────────────┬─────────────────┘
                   │
                   ▼
 ┌───────────────────────────────────┐
 │ MongoDB Data Lake Landing Zone    │
 └─────────────────┬─────────────────┘
                   │
                   ▼
 ┌───────────────────────────────────┐
 │ Aggregation Stream Audit          │
 └───────────────────────────────────┘

```

1. **Environment Setup & Connection Driver (`02_mongo_driver.py`):**
* Dynamically loads MongoDB connection strings and database credentials from `.env`.
* Manages client lifecycle with automatic connection cleanup.


2. **Ingestion & Data Staging (`03_raw_ingest_lake.py`):**
* Reads raw JSON telemetry payloads (`raw_telemetry_payloads.json`) or falls back to synthetic multi-stream mock generators.
* Stamps every landed payload with UTC timestamps (`ingested_at`).
* Performs high-throughput `insert_many` bulk operations into the landing collection.


3. **Data Lake Aggregation Audit:**
* Runs MongoDB aggregation pipelines (`04_lake_audit_queries.json`) to profile document distribution across stream sources (`WEB_STORE`, `POS_TERMINALS`, `MOBILE_APP`).
* Output trace logs are mirrored simultaneously to terminal and `lake_ingest_execution.log`.



## 🚀 How to Run

1. **Configure Environment Variables:**
Create a `.env` file in the project root:
```env
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=juanmart_datalake
MONGO_COLLECTION=raw_landing

```


2. **Install Dependencies:**
```bash
pip install pymongo python-dotenv

```


3. **Initialize MongoDB Landing Collection:**
```bash
mongosh < 01_datalake_setup.mongodb.js

```


4. **Execute Ingestion & Audit Pipeline:**
```bash
python 03_raw_ingest_lake.py

```



```

---

### Quick Folder Checklist:
1. Fix the `logging.basicConfig` line in `03_raw_ingest_lake.py`.
2. Save `README.md` in the folder root[cite: 10].
3. Add `.gitignore` to hide `.env` and `__pycache__`[cite: 10].
4. Rename `Activity2` to `mongodb-datalake-stream-ingestion`[cite: 10].

Project #6 is standardized! Do you have a 7th folder left in `DA - Projects`[cite: 1], or does this wrap up all your repositories?

```