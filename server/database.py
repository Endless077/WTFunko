from pymongo import MongoClient
from logger import get_logger

def get_database():
    if Database._instance is None:
        # Singleton instantiation, first time.
        Database()
    return Database._instance

def shutdown():
    Database._client.close()

class Database(object):
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._client = MongoClient("mongodb://localhost:27017/")
            db_name = "WTFunko"
            cls._instance = cls._client[db_name]
        return cls._instance
    
    
 