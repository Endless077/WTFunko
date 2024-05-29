# Logging System
from server.fastapi import LOG_SYS

# HTTPException
from fastapi import HTTPException
# MongoDB
import pymongo
from bson import ObjectId
from pymongo import MongoClient

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

async def get_user(username: str, email: str) -> User:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Select collection
        collection = db["Users"]
        
        # Execute the query to find the user in the collection
        LOG_SYS.write(TAG, f"Query to get user information by username: {username} or email: {email} executing.")
        user_data = collection.find_one({"$or": [{"Username": username}, {"Email": email}]})

        # If the user is not found in the database, raise an exception
        if user_data is None:
            LOG_SYS.write(TAG, f"Query to get user information by username: {username} or email: {email} failed, user not found.")
            raise HTTPException(status_code=404, detail="User not found.")

        # Build an instance of User using the data retrieved from the database
        LOG_SYS.write(TAG, f"Query to get user information by username: {username} or email: {email} success.")
        user = User(**user_data)

        return user
    except Exception as e:
        LOG_SYS.write(TAG, f"Query to get user information by username: {username} or email: {email} failed with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to getting user data.")
    finally:
        # Close the MongoDB connection
        client.close()


async def insert_user(user_data: User) -> str:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Select collection
        collection = db["Users"]
        
        # Check if the user already exists
        existing_user = collection.find_one({"Username": user_data.Username})
        if existing_user:
            LOG_SYS.write(TAG, f"Insert new user with username: {user_data.Username} failed, user already exists.")
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Insert user data into the collection
        result = collection.insert_one(user_data.model_dump())
        return "User inserted successfully."
    
    except Exception as e:
        LOG_SYS.write(TAG, f"Failed to insert user data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to insert user data.")
    finally:
        # Close the MongoDB connection
        client.close()

async def delete_user(username: str) -> str:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Select collection
        collection = db["Users"]
        
        # Delete user data from the collection
        LOG_SYS.write(TAG, f"Deleting user data with username: {username} from the database.")
        result = collection.delete_one({"Username": username})
        
        # Check if user was found and deleted
        if result.deleted_count == 0:
            LOG_SYS.write(TAG, f"Delete existing user with username: {username} failed, user not found.")
            raise HTTPException(status_code=404, detail="User not found")

        # Return success message
        LOG_SYS.write(TAG, "User data deleted successfully.")
        return "User deleted successfully."
    
    except Exception as e:
        LOG_SYS.write(TAG, f"Failed to delete user data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to delete user data.")
    finally:
        # Close the MongoDB connection
        client.close()

async def update_user(user_data: User) -> str:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Select collection
        collection = db["Users"]
        
        # Update user data in the collection
        LOG_SYS.write(TAG, f"Updating user data with username: {user_data.Username} in the database.")
        result = collection.update_one({"Username": user_data.Username}, {"$set": user_data.model_dump()})
        
        # Check if user was found and updated
        if result.matched_count == 0:
            LOG_SYS.write(TAG, f"Delete existing user with username: {username} failed, user not found.")
            raise HTTPException(status_code=404, detail="User not found")

        # Return success message
        LOG_SYS.write(TAG, "User data updated successfully.")
        return "User updated successfully."
    
    except Exception as e:
        LOG_SYS.write(TAG, f"Failed to update user data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to update user data.")
    finally:
        # Close the MongoDB connection
        client.close()

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