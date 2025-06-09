import pymongo
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)


def get_mongo_collection():
    load_dotenv()
    USER = os.getenv("MONGO_USER")
    PASS = os.getenv("MONGO_PASSWORD")
    HOST = os.getenv("MONGO_CLUSTER")
    uri = f"mongodb+srv://{USER}:{PASS}@{HOST}.j4waz.mongodb.net/Bots?retryWrites=true&w=majority"
    try:
        client = pymongo.MongoClient(uri)
        logging.info("Connected to db successfully!")
        db = client["Bots"]
        collection = db["Chuchu"]
        return collection
    except pymongo.errors.PyMongoError as e:
        logging.error(f"DB error: {e}")
        return "Failed"
