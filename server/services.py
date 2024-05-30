# Logging System
from server.fastapi import LOG_SYS

# HTTPException
from fastapi import HTTPException

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
        create_database("localhost", 27107, db_name, collections)
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
        # Collection Users
        collection = db["Users"]
        
        # Execute the query to find the user in the collection by username or password
        LOG_SYS.write(TAG, f"Query to get user information by username: {username} or email: {email} executing.")
        user_data = collection.find_one({"$or": [{"username": username}, {"Email": email}]})

        # If the user is not found in the database, raise an exception
        if user_data is None:
            LOG_SYS.write(TAG, f"Query to get user information by username: {username} or email: {email} failed, user not found.")
            raise HTTPException(status_code=404, detail="User not found.")

        # Build an instance of User using the data retrieved from the database
        LOG_SYS.write(TAG, f"Query to get user information by username: {username} or email: {email} success.")
        user = User(**user_data)
        return user
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Query to get user information by username: {username} or email: {email} failed with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to getting user data.")
    finally:
        # Close the MongoDB connection
        client.close()


async def insert_user(user_data: User) -> str:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Collection Users
        collection = db["Users"]
        
        # Check if the user already exists
        existing_user = collection.find_one({"username": user_data.username})
        if existing_user:
            LOG_SYS.write(TAG, f"Insert new user with username: {user_data.username} failed, user already exists.")
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Insert user data into the collection
        result = collection.insert_one(user_data.model_dump())
        
        # Return success message
        LOG_SYS.write(TAG, "User data insert successfully.")
        return "User inserted successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Failed to insert user data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to insert user data.")
    finally:
        # Close the MongoDB connection
        client.close()

async def delete_user(username: str) -> str:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Collection Users
        collection = db["Users"]
        
        # Delete user data from the collection
        LOG_SYS.write(TAG, f"Deleting user data with username: {username} from the database.")
        result = collection.delete_one({"username": username})
        
        # Check if user was found and deleted
        if result.deleted_count == 0:
            LOG_SYS.write(TAG, f"Delete existing user with username: {username} failed, user not found.")
            raise HTTPException(status_code=404, detail="User not found")

        # Return success message
        LOG_SYS.write(TAG, "User data deleted successfully.")
        return "User deleted successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Failed to delete user data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to delete user data.")
    finally:
        # Close the MongoDB connection
        client.close()

async def update_user(user_data: User) -> str:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Collection Users
        collection = db["Users"]
        
        # Update user data in the collection
        LOG_SYS.write(TAG, f"Updating user data with username: {user_data.username} in the database.")
        result = collection.update_one({"username": user_data.username}, {"$set": user_data.model_dump()})
        
        # Check if user was found and updated
        if result.matched_count == 0:
            LOG_SYS.write(TAG, f"Updating existing user with username: {user_data.username} failed, user not found.")
            raise HTTPException(status_code=404, detail="User not found")

        # Return success message
        LOG_SYS.write(TAG, "User data updated successfully.")
        return "User updated successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Failed to update user data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to update user data.")
    finally:
        # Close the MongoDB connection
        client.close()

###################################################################################################

async def get_orders(username: str) -> List[Order]:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Select collection
        collection = db["Orders"]
        
        # Query to find user orders in the collection by username and sort by date in descending order
        LOG_SYS.write(TAG, f"Query to get orders for username: {username} executing.")
        orders_data = list(collection.find({"user.username": username}).sort("date", -1))

        # Check if orders were found
        if not orders_data:
            LOG_SYS.write(TAG, f"No orders found for username: {username}.")
            raise HTTPException(status_code=404, detail="Orders not found.")

        # Add orders in a list
        orders = [Order(**order) for order in orders_data]
        
        # Return the user orders list
        LOG_SYS.write(TAG, f"Found {len(orders)} for user: {username}")
        return orders
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Query to get orders for username: {username} failed with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to get orders.")
    finally:
        # Close the MongoDB connection
        client.close()


async def get_order_info(order_id: str) -> Order:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Select collection
        collection = db["Orders"]
        
        # Query to find order info in the collection by uid
        LOG_SYS.write(TAG, f"Query to get order info for uid: {order_id} executing.")
        order_data = collection.find_one({"uid": order_id})

        # Check if order was found
        if order_data is None:
            LOG_SYS.write(TAG, f"Order with ID: {order_id} not found.")
            raise HTTPException(status_code=404, detail="Order not found.")

        # Return the order infos
        order = Order(**order_data)
        return order
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Query to get order info for uid: {order_id} failed with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to get order info.")
    finally:
        # Close the MongoDB connection
        client.close()

async def insert_order(order_data: Order) -> str:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Select collection
        collection = db["Orders"]

        # Query to find if order already exist
        existing_order = collection.find_one({"uid": order_data.uid})
        
        # Check if order already exist
        if existing_order:
            LOG_SYS.write(TAG, f"Insert order with uid: {order_data.uid} failed, order already exists.")
            raise HTTPException(status_code=400, detail="Order already exists")

        # Insert new data into database
        result = collection.insert_one(order_data.model_dump())
        
        # Return success message
        LOG_SYS.write(TAG, "Order data insert successfully.")
        return "Order inserted successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Failed to insert order data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to insert order data.")
    finally:
        # Close the MongoDB connection
        client.close()

async def delete_order(order_id: str) -> str:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Select collection
        collection = db["Orders"]
        
        LOG_SYS.write(TAG, f"Deleting order data with uid: {order_id} from the database.")
        result = collection.delete_one({"uid": order_id})

        if result.deleted_count == 0:
            LOG_SYS.write(TAG, f"Delete existing order with uid: {order_id} failed, order not found.")
            raise HTTPException(status_code=404, detail="Order not found")

        # Return success message
        LOG_SYS.write(TAG, "Order data deleted successfully.")
        return "Order deleted successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Failed to delete order data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to delete order data.")
    finally:
        # Close the MongoDB connection
        client.close()

async def update_order(order_data: Order) -> str:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Select collection
        collection = db["Orders"]
        
        LOG_SYS.write(TAG, f"Updating order data with uid: {order_data.uid} in the database.")
        result = collection.update_one({"uid": order_data.uid}, {"$set": order_data.model_dump()})

        if result.matched_count == 0:
            LOG_SYS.write(TAG, f"Updating existing order with uid: {order_data.uid} failed, order not found.")
            raise HTTPException(status_code=404, detail="Order not found")

        # Return success message
        LOG_SYS.write(TAG, "Order data updated successfully.")
        return "Order updated successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Failed to update order data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to update order data.")
    finally:
        # Close the MongoDB connection
        client.close()

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