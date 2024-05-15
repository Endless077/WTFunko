# MongoDB
from pymongo import MongoClient

class MongoDBManager:
    def __init__(self, host=None, port=None, db_name=None, collection_name=None):
        """
        Initialize MongoDBManager with connection details.
        :param host: MongoDB server host address.
        :param port: MongoDB server port.
        :param db_name: Name of the database.
        :param collection_name: Name of the collection.
        """
        self.host = host
        self.port = port
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.database = None
        self.collection = None

    def connect(self):
        """
        Establish connection to MongoDB server and select database & collection.
        """
        try:
            self.client = MongoClient(self.host, self.port)
            if self.db_name:
                self.database = self.client[self.db_name]
                if self.collection_name:
                    self.collection = self.database[self.collection_name]
            print("Connected to MongoDB.")
        except Exception as e:
            print("Error connecting to MongoDB:", e)

    def find_documents(self):
        """
        Retrieve all documents from the specified collection.
        :return: Cursor to the documents.
        """
        try:
            if self.collection:
                documents = self.collection.find()
                return documents
            else:
                print("Collection not specified.")
        except Exception as e:
            print("Error fetching documents:", e)

    def close_connection(self):
        """
        Close the connection to MongoDB server.
        """
        if self.client:
            self.client.close()
            print("Connection to MongoDB closed.")
