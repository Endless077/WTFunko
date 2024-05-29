# Services
import pymongo
from bson import ObjectId
from pymongo import MongoClient

# Logging System
from server.fastapi import LOG_SYS

# Other utils
from server.models import *
from server.mongoDB import *

TAG = "Services"
###################################################################################################

# Init Database
async def init_database(db_name, collections):
    # Check if the database already exists
    if not check_database_exists(db_name):
        # If the database doesn't exist, create a new database
        LOG_SYS.write(TAG, f"Database '{db_name}' does not exist.")
        LOG_SYS.write(TAG, "Creating new database.")
        create_database(db_name, collections)
    else:
        # If the database exists, check for missing collections
        LOG_SYS.write(TAG, f"Database '{db_name}' exists.")
        missing_collections = []
        for collection in collections:
            if not check_collection_exists(db_name, collection):
                missing_collections.append(collection)
        
        # If there are missing collections, create them
        if missing_collections:
            client, db = connect(db_name)
            for collection in missing_collections:
                db.create_collection(collection)
            LOG_SYS.write(TAG, f"Missing collections created: {', '.join(missing_collections)}")
        else:
            # Otherwise, all collections are present
            LOG_SYS.write(TAG, f"All collections {', '.join(collections)} are present.")
    
    # Report completion of database initialization
    LOG_SYS.write(TAG, f"Initialization completed for database '{db_name}'.")
    
    
###################################################################################################

async def get_user(username: str, password: str) -> User:
    pass

async def insert_user(user_data: User) -> str:
    pass

async def delete_user(username: str) -> str:
    pass

async def update_user(user_data: User) -> str:
    pass

###################################################################################################

async def get_orders(username: str) -> List[Order]:
    pass

async def get_order_info(order_id: str) -> Order:
    pass

async def insert_order(order_data: Order) -> str:
    pass

async def delete_order(order_id: str) -> str:
    pass

async def update_order(order_data: User) -> str:
    pass

###################################################################################################

def get_all_funkos() -> List[Product]:
    pass

def get_funko_info(funk_id: str) -> Product:
    pass

def get_funko_by_category(category: str) -> List[Product]:
    pass

def get_funko_by_search(search_string: str) -> List[Product]:
    pass

def sort_funko(criteria: str) -> List[Product]:
    pass

def insert_funko(funko: Product) -> str:
    pass

def delete_funko(funk_id: str) -> str:
    pass

def update_funko(funko: Product) -> str:
    pass

###################################################################################################