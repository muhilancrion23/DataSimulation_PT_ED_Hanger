import IPython.core.formatters
from dateutil.tz import UTC
from pymongo import MongoClient
from datetime import datetime, timedelta
import numpy as np
from bson import ObjectId
from slowchangevalues import generate_slow_values
import dotenv

dotenv.load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
TAG_COLLECTION = os.getenv("TAG_COLLECTION")
LIVE_COLLECTION = os.getenv("LIVE_COLLECTION")

PLC_NAME = "DEFAULT_PLC"
SECONDS = 86400
START_TIME = datetime(2026,2,20,18,30,0,tzinfo=UTC)


TAGS_CONFIG = []

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

tags_col = db[TAG_COLLECTION]
live_col = db[LIVE_COLLECTION]

def generate_and_store():
    now = datetime.now()

    for tag in TAGS_CONFIG:

        tag_doc = {
            "asset_id": [],
            "tagname": tag["tagname"],
            "latestValue": None,
            "unit": tag["unit"],
            "datatype": tag["datatype"],
            "plcName": PLC_NAME,
            "isActive": True,
            "health":True,
            "plcMeta":{
                "dbaddress": 1,
            },
            "ranges": {
                "minValue": tag["min"],
                "maxValue": tag["max"]
            },
            "createdAt": now,
            "updatedAt": None
        }

        tag_id = tags_col.insert_one(tag_doc).inserted_id

        values = generate_slow_values(tag["min"], tag["max"], SECONDS)
        bulk_live = []

        for i, val in enumerate(values):
            bulk_live.append({
                "tag_id": tag_id,
                "timestamp": START_TIME + timedelta(seconds=i),
                "value": val
            })

        live_col.insert_many(bulk_live)

        latest_value = values[-1]
        latest_timestamp = START_TIME + timedelta(seconds=SECONDS - 1)

        tags_col.update_one(
            {"_id": tag_id},
            {
                "$set": {
                    "latestValue": latest_value,
                    "updatedAt": latest_timestamp,
                }
            }
        )

        print(f"✅ Tag generated: {tag['tagname']}")

if __name__ == "__main__":
    generate_and_store()
    print("\n🎯 Time-series data generation completed successfully.")
