from dateutil.tz import UTC
from pymongo import MongoClient
from datetime import datetime, timedelta
import numpy as np
import random
from slowchangevalues import generate_slow_values
import dotenv

dotenv.load_dotenv()

# ==============================
# CONFIG
# ==============================

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
TAG_COLLECTION = os.getenv("TAG_COLLECTION")
LIVE_COLLECTION = os.getenv("LIVE_COLLECTION")
DATA_START_TIME = datetime(2026, 2, 13, 18, 30, 0,tzinfo=UTC)
# ==============================
# MULTI TAG UPDATE FUNCTION
# ==============================

def insert_synthetic_multiple_tags(tag_names, start_time, seconds):

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    if LIVE_COLLECTION not in db.list_collection_names():
        db.create_collection(
            LIVE_COLLECTION,
            timeseries={
                "timeField": "timestamp",
                "metaField": "tag_id",
                "granularity": "seconds"
            }
        )
        print(f"✅ Time-series collection '{LIVE_COLLECTION}' created.")
    tags_col = db[TAG_COLLECTION]
    live_col = db[LIVE_COLLECTION]

    for tagname in tag_names:

        tag_doc = tags_col.find_one({"tagname": tagname})

        if not tag_doc:
            print(f"❌ Tag '{tagname}' not found. Skipping.")
            continue

        tag_id = tag_doc["_id"]
        min_val = tag_doc["ranges"]["minValue"]
        max_val = tag_doc["ranges"]["maxValue"]

        values = generate_slow_values(min_val, max_val, seconds)

        bulk_data = []

        for i, val in enumerate(values):
            bulk_data.append({
                "tag_id": tag_id,
                "timestamp": DATA_START_TIME + timedelta(seconds=i),
                "value": val
            })

        if bulk_data:
            live_col.insert_many(bulk_data)

            latest_value = values[-1]
            latest_timestamp = DATA_START_TIME + timedelta(seconds=seconds - 1)

            tags_col.update_one(
                {"_id": tag_id},
                {
                    "$set": {
                        "latestValue": latest_value,
                        "updatedAt": latest_timestamp
                    }
                }
            )

        print(f"✅ Inserted {seconds} values for '{tagname}'")

    print("\n🎯 Multi-tag synthetic update completed.")


# ==============================
# RUN
# ==============================

if __name__ == "__main__":

    TAGS_TO_UPDATE =['']    
    insert_synthetic_multiple_tags(tag_names=TAGS_TO_UPDATE,start_time=DATA_START_TIME,seconds=691200)
