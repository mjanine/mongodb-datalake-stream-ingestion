# 02_mongo_driver.py
import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s,%(msecs)03d - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

class MongoDriver:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDriver, cls).__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        self.uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.db_name = os.getenv("DB_NAME", "juanmart_data_lake")
        
        logger.info("Initializing Data Lake MongoClient connection pool...")
        try:
            # Connection pooling with defensive timeouts
            self.client = MongoClient(
                self.uri,
                maxPoolSize=50,
                minPoolSize=10,
                serverSelectionTimeoutMS=5000
            )
            # Health check ping
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            logger.info(f"[+] Successfully established Data Lake connection to: {self.db_name}")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"[-] Database connection failed: {e}")
            raise

    def get_collection(self, collection_name=None):
        coll_name = collection_name or os.getenv("COLLECTION_NAME", "raw_checkout_landing")
        return self.db[coll_name]

    def close(self):
        if self.client:
            self.client.close()
            logger.info("[+] Data Lake MongoClient connection pool gracefully closed.")

if __name__ == "__main__":
    driver = MongoDriver()
    driver.close()