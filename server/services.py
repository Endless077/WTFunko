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
        
        # Insert one new user data into the collection
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
        # Collection Orders
        collection = db["Orders"]
        
        # Query to find user orders in the collection by username and sort by date in descending order
        LOG_SYS.write(TAG, f"Query to get orders for username: {username} executing.")
        orders_data = list(collection.find({"user.username": username}).sort("date", -1))

        # Check if orders were found
        if not orders_data:
            LOG_SYS.write(TAG, f"No orders found for username: {username}.")
            raise HTTPException(status_code=404, detail="Orders not found.")

        # Build a list of instance of Orders using the data retrieved from the database
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
        # Collection Orders
        collection = db["Orders"]
        
        # Query to find order info in the collection by uid
        LOG_SYS.write(TAG, f"Query to get order info for uid: {order_id} executing.")
        order_data = collection.find_one({"uid": order_id})

        # Check if order was found
        if order_data is None:
            LOG_SYS.write(TAG, f"Order with ID: {order_id} not found.")
            raise HTTPException(status_code=404, detail="Order not found.")

        # Build an instance of Order using the data retrieved from the database
        order = Order(**order_data)
        
        # Return the order infos
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
        # Collection Orders
        collection = db["Orders"]

        # Query to find if order already exist
        existing_order = collection.find_one({"uid": order_data.uid})
        
        # Check if order already exist
        if existing_order:
            LOG_SYS.write(TAG, f"Insert order with uid: {order_data.uid} failed, order already exists.")
            raise HTTPException(status_code=400, detail="Order already exists")

        # Insert one new order data into database
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
        # Collection Orders
        collection = db["Orders"]
        
        # Delete one funcion to update the new order infos
        LOG_SYS.write(TAG, f"Deleting order data with uid: {order_id} from the database.")
        result = collection.delete_one({"uid": order_id})

        # Check if order was found and deleted
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
        # Collection Orders
        collection = db["Orders"]
        
        # Update one funcion to update the new order infos
        LOG_SYS.write(TAG, f"Updating order data with uid: {order_data.uid} in the database.")
        result = collection.update_one({"uid": order_data.uid}, {"$set": order_data.model_dump()})

        # Check if order was found and updated
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

async def get_all_products() -> List[Product]:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Collection Orders
        collection = db["Products"]
        
        # Query to find all products in the collection
        LOG_SYS.write(TAG, "Query to get all products executing.")
        product_data = list(collection.find())

        # Check if Products were found
        if not product_data:
            LOG_SYS.write(TAG, "No Products found.")
            return []

        # Build a list of instances of Product using the data retrieved from the database
        products = [Product(**product) for product in product_data]
        
        # Return the list of Funkos
        LOG_SYS.write(TAG, f"Found {len(products)} products.")
        return products
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Query to get all products failed with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to get products.")
    finally:
        # Close the MongoDB connection
        client.close()

async def get_product_info(product_id: str) -> Product:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Collection Orders
        collection = db["Products"]
        
        # Query to find Funko info in the collection by uid
        LOG_SYS.write(TAG, f"Query to get products info for uid: {product_id} executing.")
        products_data = collection.find_one({"uid": product_id})

        # Check if Funko was found
        if products_data is None:
            LOG_SYS.write(TAG, f"Product with uid: {product_id} not found.")
            raise HTTPException(status_code=404, detail="Product not found.")

        # Build an instance of Product using the data retrieved from the database
        product = Product(**products_data)
        
        # Return the Funko info
        return product
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Query to get Funko info for uid: {product_id} failed with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to get Funko info.")
    finally:
        # Close the MongoDB connection
        client.close()

async def get_product_by_category(category: str) -> List[Product]:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Collection Products
        collection = db["Products"]
        
        # Query to find products by category in the collection
        LOG_SYS.write(TAG, f"Query to get products by category '{category}' executing.")
        product_data = list(collection.find({"interest": {"$in": [category]}}))

        # Check if Products were found
        if not product_data:
            LOG_SYS.write(TAG, f"No Products found for category '{category}'.")
            return []

        # Build a list of instances of Product using the data retrieved from the database
        products = [Product(**product) for product in product_data]
        
        # Return the list of products
        LOG_SYS.write(TAG, f"Found {len(products)} products for category '{category}'.")
        return products
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Query to get products by category '{category}' failed with error: {e}.")
        raise HTTPException(status_code=500, detail=f"Failed to get products by category '{category}'.")
    finally:
        # Close the MongoDB connection
        client.close()

async def get_product_by_search(search_string: str) -> List[Product]:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Collection Products
        collection = db["Products"]
        
        # Query to find products by search string in the title
        LOG_SYS.write(TAG, f"Query to get products by search string '{search_string}' executing.")
        product_data = list(collection.find({"title": {"$regex": f".*{search_string}.*", "$options": "i"}}))

        # Check if Products were found
        if not product_data:
            LOG_SYS.write(TAG, f"No Products found for search string '{search_string}'.")
            return []

        # Build a list of instances of Product using the data retrieved from the database
        products = [Product(**product) for product in product_data]
        
        # Return the list of products
        LOG_SYS.write(TAG, f"Found {len(products)} products for search string '{search_string}'.")
        return products
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Query to get products by search string '{search_string}' failed with error: {e}.")
        raise HTTPException(status_code=500, detail=f"Failed to get products by search string '{search_string}'.")
    finally:
        # Close the MongoDB connection
        client.close()

async def sort_product(criteria: str, price: float = None, asc: bool = True) -> List[Product]:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Collection Products
        collection = db["Products"]
        
        # Define sorting order
        sort_order = 1 if asc else -1

        # Define sorting criteria and query filter in a more compact way
        query_filter = {"price": {"$lte": price}} if criteria == "price" and price is not None else {}
        sort_criteria = [("price", sort_order)] if criteria == "price" else [("title", sort_order)]
        
        # Query to sort products by criteria and order
        LOG_SYS.write(TAG, f"Query to sort products by criteria '{criteria}' in {'ascending' if asc else 'descending'} order executing.")
        product_data = list(collection.find(query_filter).sort(sort_criteria))

        # Check if Products were found
        if not product_data:
            LOG_SYS.write(TAG, f"No Products found for sorting criteria '{criteria}' in {'ascending' if asc else 'descending'} order.")
            return []

        # Build a list of instances of Product using the data retrieved from the database
        products = [Product(**product) for product in product_data]
        
        # Return the list of sorted products
        LOG_SYS.write(TAG, f"Sorted {len(products)} products by criteria '{criteria}' in {'ascending' if asc else 'descending'} order.")
        return products
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Query to sort products by criteria '{criteria}' in {'ascending' if asc else 'descending'} order failed with error: {e}.")
        raise HTTPException(status_code=500, detail=f"Failed to sort products by criteria '{criteria}' in {'ascending' if asc else 'descending'} order.")
    finally:
        # Close the MongoDB connection
        client.close()

async def filter_product(category: str = None, search_string: str = None, criteria: str = None, price: float = None, asc: bool = True) -> List[Product]:
    products = []

    # Filter by category if specified
    if category:
        LOG_SYS.write(TAG, f"Filtering products by category '{category}'")
        products = await get_product_by_category(category)

    # Filter by search string if specified
    if search_string:
        LOG_SYS.write(TAG, f"Filtering products by search string '{search_string}'")
        search_results = await get_product_by_search(search_string)
        if products:
            # Intersect the two lists based on product uid
            products_uids = {product.uid for product in products}
            products = [product for product in search_results if product.uid in products_uids]
        else:
            products = search_results

    # Eliminate duplicates
    unique_products = {product.uid: product for product in products}.values()

    # Sort products if a sorting criterion is specified
    if criteria:
        LOG_SYS.write(TAG, f"Sorting products by criteria '{criteria}'")
        # If the criteria is "price" and price is specified, call the sorting function directly
        if criteria == "price" and price is not None:
            products = await sort_product(criteria="price", price=price, asc=asc)
        else:
            # If products are already filtered, apply sorting to these products
            if unique_products:
                sort_order = 1 if asc else -1
                unique_products = sorted(unique_products, key=lambda x: x.price if criteria == "price" else x.title, reverse=not asc)
            else:
                # If there are no previously filtered products, call the sorting function without price
                products = await sort_product(criteria=criteria, asc=asc)

    return list(unique_products)

async def insert_product(product_data: Product) -> str:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Collection Products
        collection = db["Products"]
        
        # Check if the product already exists
        existing_product = collection.find_one({"uid": product_data.uid})
        if existing_product:
            LOG_SYS.write(TAG, f"Insert product with uid: {product_data.uid} failed, product already exists.")
            raise HTTPException(status_code=400, detail="Product already exists")
        
        # Insert one new product data into the collection
        result = collection.insert_one(product_data.model_dump())
        
        # Return success message
        LOG_SYS.write(TAG, "Product data insert successfully.")
        return "Product inserted successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Failed to insert product data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to insert product data.")
    finally:
        # Close the MongoDB connection
        client.close()

async def delete_product(product_id: str) -> str:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Collection Products
        collection = db["Products"]
        
        # Delete product data from the collection
        LOG_SYS.write(TAG, f"Deleting product data with uid: {product_id} from the database.")
        result = collection.delete_one({"uid": product_id})
        
        # Check if product was found and deleted
        if result.deleted_count == 0:
            LOG_SYS.write(TAG, f"Delete existing product with uid: {product_id} failed, product not found.")
            raise HTTPException(status_code=404, detail="Product not found")

        # Return success message
        LOG_SYS.write(TAG, "Product data deleted successfully.")
        return "Product deleted successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Failed to delete product data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to delete product data.")
    finally:
        # Close the MongoDB connection
        client.close()

async def update_product(product_data: Product) -> str:
    LOG_SYS.write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect(DB_NAME, URI)
    try:
        # Collection Products
        collection = db["Products"]
        
        # Update product data in the collection
        LOG_SYS.write(TAG, f"Updating product data with uid: {product_data.uid} in the database.")
        result = collection.update_one({"uid": product_data.uid}, {"$set": product_data.model_dump()})
        
        # Check if product was found and updated
        if result.matched_count == 0:
            LOG_SYS.write(TAG, f"Updating existing product with uid: {product_data.uid} failed, product not found.")
            raise HTTPException(status_code=404, detail="Product not found")

        # Return success message
        LOG_SYS.write(TAG, "Product data updated successfully.")
        return "Product updated successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        LOG_SYS.write(TAG, f"Failed to update product data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to update product data.")
    finally:
        # Close the MongoDB connection
        client.close()

###################################################################################################