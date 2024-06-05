"""
Handles methods and services involving mongoDB.
"""

import json
import os

from pymongo import MongoClient
from logger import get_logger
from database import get_database
from fastapi import HTTPException
from server.models import *
from server.mongo import *

LOG_SYS = get_logger()
DB = get_database()
TAG = "Mongo"

# Example of MongoDB URI "mongodb://username:password@mongodb.example.com:27017"
URI = "mongodb://username:password@mongodb.example.com:27017"

async def connect_to_database():
    # if username is None or password is None:
    #     client = MongoClient(host, port)
    #     URI = f"mongodb://{host}:{port}/{db_name}"
    # else:
    #     client = MongoClient(host, port, username=username, password=password)
    #     URI = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
    try:
        global DB
        DB = get_database()
        LOG_SYS.write(TAG, "Connected to MongoDB.")
    except Exception as e:
        LOG_SYS.write(TAG, "Error connecting to MongoDB: ", e)


def read_json(json_file):
    if not os.path.exists(json_file):
        LOG_SYS.write(TAG, f"File '{json_file}' not found.")
        return
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except Exception as e:
        LOG_SYS.write(TAG, "Error filling collection:", e)
        
    return data


async def populate_database_from_initial_dataset():
    funko_pops_dataset_path = '../source/json/products.json'
    funko_pops_dataset = read_json(funko_pops_dataset_path)
    products = DB["Products"]
    count = products.count_documents({})
    if count > 0:
        LOG_SYS.write(TAG, "A collection for funko pops already exists.")
        return
    data = list(funko_pops_dataset.values())
    result = products.insert_many(data)
    #collection_names = db.list_collection_names()
    LOG_SYS.write(TAG, f"Filled the funko pops collection with {len(result.inserted_ids)} documents.")
    

async def get_all_products() -> List[Product]:
    try:
        products = DB["Products"]
        LOG_SYS.write(TAG, "Query to get all products executing.")
        product_data = list(products.find())
        if not product_data:
            LOG_SYS.write(TAG, "No Products found.")
            return []
        # Build a list of instances of Product using the data retrieved from the database
        products = [Product(**product) for product in product_data]
        LOG_SYS.write(TAG, f"Found {len(products)} products.")
        return products
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Query to get all products failed with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to get products.")


async def get_product(product_id) -> Product:
    try:
        products = DB["Products"]
        # Query to find Funko info in the collection by uid
        LOG_SYS.write(TAG, f"Query to get products info for uid: {product_id} executing.")
        products_data = products.find_one({"_id": product_id})
        if products_data is None:
            LOG_SYS.write(TAG, f"Product with id: {product_id} not found.")
            raise HTTPException(status_code=404, detail="Product not found.")
        # Build an instance of Product using the data retrieved from the database
        product = Product(**products_data)
        print("Hello")
        print(type(products_data["_id"]))
        print(products_data)
        print("------")
        print(product)
        return product

    except Exception as e:
        LOG_SYS.write(TAG, f"Query to get Funko info for uid: {product_id} failed with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to get Funko info.")