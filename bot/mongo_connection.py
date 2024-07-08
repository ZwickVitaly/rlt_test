from pymongo import MongoClient
from settings import DB_HOST, MONGO_PASSWORD, MONGO_USER, logger

logger.debug("Init mongo")
client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{DB_HOST}:27017/")

logger.debug("Find collection")
collection = client["sample_collection"]["sample_collection"]


MONGO_PIPE = [
    {
        "$match": {"dt": None},
    },
    {
        "$group": {
            "_id": {"$dateTrunc": {"date": "$dt", "unit": None}},
            "value": {"$sum": "$value"},
        },
    },
    {"$sort": {"_id": 1}},
    {"$densify": {"field": "_id", "range": {"step": 1, "unit": None, "bounds": None}}},
    {
        "$group": {
            "_id": None,
            "dataset": {"$push": {"$ifNull": ["$value", 0]}},
            "labels": {
                "$push": {
                    "$dateToString": {"date": "$_id", "format": "%Y-%m-%dT%H:%M:%S"}
                }
            },
        }
    },
    {"$unset": "_id"},
]
