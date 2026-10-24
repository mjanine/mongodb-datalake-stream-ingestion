// 01_datalake_setup.mongodb.js
use('juanmart_data_lake');

// Create the raw landing collection
db.createCollection('raw_checkout_landing');

// Index key fields for optimized query performance
db.raw_checkout_landing.createIndex({ "stream_source": 1 });
db.raw_checkout_landing.createIndex({ "ingested_at": 1 });
db.raw_checkout_landing.createIndex({ "payload_id": 1 }, { unique: true, sparse: true });

console.log("Database and collection successfully initialized with indexes.");