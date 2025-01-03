# Database class
from pymongo import MongoClient

# Example of MongoDB URI "mongodb://username:password@mongodb.example.com:27017"
#URI = "mongodb://username:password@mongodb.example.com:27017"

URI = "mongodb://localhost:27017"
DB_NAME = "test"

class Database(object):
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._client = MongoClient(URI)
            cls._instance = cls._client[DB_NAME]
        return cls._instance

###################################################################################################

def get_database(uri="mongodb://localhost:27017", db_name="test"):
    global URI
    global DB_NAME

    URI = uri
    DB_NAME = db_name
    if Database._instance is None:
        Database()
    return Database._instance

def close_connection():
    Database._client.close()  
