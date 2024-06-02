"""
Handles methods and services involving mongoDB.
"""

import json
import os

from pymongo import MongoClient
from fastapi import HTTPException
from server.models import *
from server.mongo import *
from logger import get_logger

TAG = "Mongo"

# Example of MongoDB URI "mongodb://username:password@mongodb.example.com:27017"
URI = "mongodb://username:password@mongodb.example.com:27017"

def connect(client, db_name):
    # if username is None or password is None:
    #     client = MongoClient(host, port)
    #     URI = f"mongodb://{host}:{port}/{db_name}"
    # else:
    #     client = MongoClient(host, port, username=username, password=password)
    #     URI = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
    try:
        if db_name:
            database = client[db_name]
            get_logger().write(TAG, "Connected to MongoDB.")
    except Exception as e:
           get_logger().write(TAG, "Error connecting to MongoDB: ", e)
        
    return database


def read_json(json_file):
    if not os.path.exists(json_file):
        get_logger().write(TAG, f"File '{json_file}' not found.")
        return
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except Exception as e:
        get_logger().write(TAG, "Error filling collection:", e)
        
    return data


def populate_database_from_initial_dataset(db):
    funko_pops_dataset_path = '../source/json/products.json'
    funko_pops_dataset = read_json(funko_pops_dataset_path)
    products = db["Products"]
    count = products.count_documents({})
    if count > 0:
        get_logger().write(TAG, "A collection for funko pops already exists.")
        return
    data = list(funko_pops_dataset.values())
    result = products.insert_many(data)
    #collection_names = db.list_collection_names()
    get_logger().write(TAG, f"Filled the funko pops collection with {len(result.inserted_ids)} documents.")
    

async def get_all_products(db) -> List[Product]:
    try:
        products = db["Products"]
        get_logger().write(TAG, "Query to get all products executing.")
        product_data = list(products.find())
        if not product_data:
            get_logger().write(TAG, "No Products found.")
            return []
        # Build a list of instances of Product using the data retrieved from the database
        products = [Product(**product) for product in product_data]
        get_logger().write(TAG, f"Found {len(products)} products.")
        return products
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Query to get all products failed with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to get products.")