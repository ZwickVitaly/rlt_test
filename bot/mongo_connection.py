from pymongo import MongoClient
from settings import logger, MONGO_USER, MONGO_PASSWORD, DB_HOST


logger.debug("Init mongo")
client = MongoClient(
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{DB_HOST}:27017/"
)

logger.debug("Find collection")
collection = client["sample_collection"]["sample_collection"]


MONGO_PIPE = [
        {
            "$match": {"dt": None},
        },
        {
          "$group": {
              "_id": {
                      "$dateTrunc": {
                          "date": "$dt", "unit": None
                      }
              },
              "value": {"$sum": "$value"},
          },
        },
        {
          "$sort": {"_id": 1}
        },
        {
            "$group": {
                "_id": None,
                "dataset": {"$push": "$value"},
                "labels": {"$push": {"$dateToString": {"date": "$_id", "format": "%Y-%m-%dT%H:%M:%S"}}},
            }
        },
        {
          "$unset": "_id"
        }

    ]