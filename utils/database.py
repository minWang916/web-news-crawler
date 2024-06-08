from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import MONGO_URI


def connect_to_mongo():
    """
    Establish a connection to the MongoDB server and return the client object.
    """
    try:
        print(MONGO_URI)
        client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
        client.admin.command("ping")
        print("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

MONGO_CLIENT = connect_to_mongo()
DATABASE = MONGO_CLIENT["web-news-crawler"]
LINKS_COLLECTION = DATABASE["links"]
SOURCES_COLLECTION = DATABASE["sources"]
SOURCES_BACKUP = DATABASE["sources-backup"]