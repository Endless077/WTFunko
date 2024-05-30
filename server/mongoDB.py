# Utils
import json
import os

from pymongo import MongoClient

# Example of MongoDB URI "mongodb://username:password@mongodb.example.com:27017"
URI = "mongodb://username:password@mongodb.example.com:27017"

###################################################################################################

# Establish connection to MongoDB server and select database & collection
def connect(db_name, uri=URI):
    try:
        client = MongoClient(uri)
        if db_name:
            database = client[db_name]
        print("Connected to MongoDB.")
    except Exception as e:
        print("Error connecting to MongoDB:", e)
    
    return client, database

# Fill a MongoDB collection with data from a JSON file
def fill_collection(db_name, collection_name, json_file, uri=URI):
    
    # Check if the JSON file exists
    if not os.path.exists(json_file):
        print(f"File '{json_file}' not found.")
        return
    
    try:
        # Connect to the MongoDB server
        client = MongoClient(uri)
        
        # Select the database and collection
        db = client[db_name]
        collection = db[collection_name]
        
        # Read the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        # Insert the data into the collection
        collection.insert_many(data)
        
        print(f"Data inserted into collection '{collection_name}' in database '{db_name}'.")
    except Exception as e:
        print("Error filling collection:", e)
    finally:
        # Close the connection
        client.close()

# Retrieve all documents from the specified collection
def find_documents(collection):
    try:
        if collection:
            documents = collection.find()
            return documents
        else:
            print("Collection not specified.")
    except Exception as e:
        print("Error fetching documents:", e)


# Close the connection to MongoDB server.
def close_connection(client):
    if client:
        client.close()
        print("Connection to MongoDB closed.")
        
###################################################################################################

# Check if a MongoDB database exists
def check_database_exists(db_name, uri=URI):
    client = MongoClient(uri)
    database = client.get_database(db_name)
    
    try:
        _ = database.list_collection_names()
        return True
    except Exception as e:
        print(f"Error accessing database: {e}")
        return False

# Check if a collection exists in a MongoDB database
def check_collection_exists(db_name, collection_name, uri=URI):
    client = MongoClient(uri)
    db = client[db_name]
    collection_names = db.list_collection_names()
    return collection_name in collection_names

###################################################################################################

# Create a MongoDB database
def create_database(host, port, db_name, collections, username=None, password=None):
    # Create, define and connect to the MongoDB server
    if username is None or password is None:
        client = MongoClient(host, port)
        URI = f"mongodb://{host}:{port}/{db_name}"
    else:
        client = MongoClient(host, port, username=username, password=password)
        URI = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
        
    # Check if the database already exists
    if db_name in client.list_database_names():
        print(f"The database '{db_name}' already exists.")
        return

    # Create the database
    db = client[db_name]
    print(f"The database '{db_name}' has been successfully created.")

    # Create the collections
    for collection_name in collections:
        collection = db[collection_name]
        print(f"The collection '{collection_name}' has been successfully created.")

    # Return the database object
    return db

# Delete a MongoDB database
def delete_database(db_name, uri=URI):
    client = MongoClient(uri)
    client.drop_database(db_name)
    print(f"The database {db_name} has been successfully deleted.")

###################################################################################################
