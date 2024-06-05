"""
Handles services for the interaction with the database.
"""

from logger import get_logger
from fastapi import HTTPException
from server.models import *
from server.mongo import *

TAG = "Services"

    
async def get_user(username: str, email: str) -> User:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Users
        collection = db["Users"]
        
        # Execute the query to find the user in the collection by username or password
        get_logger().write(TAG, f"Query to get user information by username: {username} or email: {email} executing.")
        user_data = collection.find_one({"$or": [{"username": username}, {"Email": email}]})

        # If the user is not found in the database, raise an exception
        if user_data is None:
            get_logger().write(TAG, f"Query to get user information by username: {username} or email: {email} failed, user not found.")
            raise HTTPException(status_code=404, detail="User not found.")

        # Build an instance of User using the data retrieved from the database
        get_logger().write(TAG, f"Query to get user information by username: {username} or email: {email} success.")
        user = User(**user_data)
        return user
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Query to get user information by username: {username} or email: {email} failed with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to getting user data.")
    finally:
        # Close the MongoDB connection
        client.close()


async def insert_user(user_data: User) -> str:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Users
        collection = db["Users"]
        
        # Check if the user already exists
        existing_user = collection.find_one({"username": user_data.username})
        if existing_user:
            get_logger().write(TAG, f"Insert new user with username: {user_data.username} failed, user already exists.")
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Insert one new user data into the collection
        result = collection.insert_one(user_data.model_dump())
        
        # Return success message
        get_logger().write(TAG, "User data insert successfully.")
        return "User inserted successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Failed to insert user data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to insert user data.")
    finally:
        # Close the MongoDB connection
        client.close()


async def delete_user(username: str) -> str:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Users
        collection = db["Users"]
        
        # Delete user data from the collection
        get_logger().write(TAG, f"Deleting user data with username: {username} from the database.")
        result = collection.delete_one({"username": username})
        
        # Check if user was found and deleted
        if result.deleted_count == 0:
            get_logger().write(TAG, f"Delete existing user with username: {username} failed, user not found.")
            raise HTTPException(status_code=404, detail="User not found")

        # Return success message
        get_logger().write(TAG, "User data deleted successfully.")
        return "User deleted successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Failed to delete user data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to delete user data.")
    finally:
        # Close the MongoDB connection
        client.close()


async def update_user(user_data: User) -> str:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Users
        collection = db["Users"]
        
        # Update user data in the collection
        get_logger().write(TAG, f"Updating user data with username: {user_data.username} in the database.")
        result = collection.update_one({"username": user_data.username}, {"$set": user_data.model_dump()})
        
        # Check if user was found and updated
        if result.matched_count == 0:
            get_logger().write(TAG, f"Updating existing user with username: {user_data.username} failed, user not found.")
            raise HTTPException(status_code=404, detail="User not found")

        # Return success message
        get_logger().write(TAG, "User data updated successfully.")
        return "User updated successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Failed to update user data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to update user data.")
    finally:
        # Close the MongoDB connection
        client.close()


async def get_orders(username: str) -> List[Order]:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Orders
        collection = db["Orders"]
        
        # Query to find user orders in the collection by username and sort by date in descending order
        get_logger().write(TAG, f"Query to get orders for username: {username} executing.")
        orders_data = list(collection.find({"user.username": username}).sort("date", -1))

        # Check if orders were found
        if not orders_data:
            get_logger().write(TAG, f"No orders found for username: {username}.")
            raise HTTPException(status_code=404, detail="Orders not found.")

        # Build a list of instance of Orders using the data retrieved from the database
        orders = [Order(**order) for order in orders_data]
        
        # Return the user orders list
        get_logger().write(TAG, f"Found {len(orders)} for user: {username}")
        return orders
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Query to get orders for username: {username} failed with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to get orders.")
    finally:
        # Close the MongoDB connection
        client.close()


async def get_order_info(order_id: str) -> Order:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Orders
        collection = db["Orders"]
        
        # Query to find order info in the collection by uid
        get_logger().write(TAG, f"Query to get order info for uid: {order_id} executing.")
        order_data = collection.find_one({"uid": order_id})

        # Check if order was found
        if order_data is None:
            get_logger().write(TAG, f"Order with ID: {order_id} not found.")
            raise HTTPException(status_code=404, detail="Order not found.")

        # Build an instance of Order using the data retrieved from the database
        order = Order(**order_data)
        
        # Return the order infos
        return order
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Query to get order info for uid: {order_id} failed with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to get order info.")
    finally:
        # Close the MongoDB connection
        client.close()

async def insert_order(order_data: Order) -> str:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Orders
        collection = db["Orders"]

        # Query to find if order already exist
        existing_order = collection.find_one({"uid": order_data._id})
        
        # Check if order already exist
        if existing_order:
            get_logger().write(TAG, f"Insert order with uid: {order_data._id} failed, order already exists.")
            raise HTTPException(status_code=400, detail="Order already exists")

        # Insert one new order data into database
        result = collection.insert_one(order_data.model_dump())
        
        # Return success message
        get_logger().write(TAG, "Order data insert successfully.")
        return "Order inserted successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Failed to insert order data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to insert order data.")
    finally:
        # Close the MongoDB connection
        client.close()

async def delete_order(order_id: str) -> str:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Orders
        collection = db["Orders"]
        
        # Delete one funcion to update the new order infos
        get_logger().write(TAG, f"Deleting order data with uid: {order_id} from the database.")
        result = collection.delete_one({"uid": order_id})

        # Check if order was found and deleted
        if result.deleted_count == 0:
            get_logger().write(TAG, f"Delete existing order with uid: {order_id} failed, order not found.")
            raise HTTPException(status_code=404, detail="Order not found")

        # Return success message
        get_logger().write(TAG, "Order data deleted successfully.")
        return "Order deleted successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Failed to delete order data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to delete order data.")
    finally:
        # Close the MongoDB connection
        client.close()

async def update_order(order_data: Order) -> str:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Orders
        collection = db["Orders"]
        
        # Update one funcion to update the new order infos
        get_logger().write(TAG, f"Updating order data with uid: {order_data._id} in the database.")
        result = collection.update_one({"uid": order_data._id}, {"$set": order_data.model_dump()})

        # Check if order was found and updated
        if result.matched_count == 0:
            get_logger().write(TAG, f"Updating existing order with uid: {order_data._id} failed, order not found.")
            raise HTTPException(status_code=404, detail="Order not found")

        # Return success message
        get_logger().write(TAG, "Order data updated successfully.")
        return "Order updated successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Failed to update order data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to update order data.")
    finally:
        # Close the MongoDB connection
        client.close()


async def get_product_by_category(category: str) -> List[Product]:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Products
        collection = db["Products"]
        
        # Query to find products by category in the collection
        get_logger().write(TAG, f"Query to get products by category '{category}' executing.")
        product_data = list(collection.find({"interest": {"$in": [category]}}))

        # Check if Products were found
        if not product_data:
            get_logger().write(TAG, f"No Products found for category '{category}'.")
            return []

        # Build a list of instances of Product using the data retrieved from the database
        products = [Product(**product) for product in product_data]
        
        # Return the list of products
        get_logger().write(TAG, f"Found {len(products)} products for category '{category}'.")
        return products
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Query to get products by category '{category}' failed with error: {e}.")
        raise HTTPException(status_code=500, detail=f"Failed to get products by category '{category}'.")
    finally:
        # Close the MongoDB connection
        client.close()

async def get_product_by_search(search_string: str) -> List[Product]:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Products
        collection = db["Products"]
        
        # Query to find products by search string in the title
        get_logger().write(TAG, f"Query to get products by search string '{search_string}' executing.")
        product_data = list(collection.find({"title": {"$regex": f".*{search_string}.*", "$options": "i"}}))

        # Check if Products were found
        if not product_data:
            get_logger().write(TAG, f"No Products found for search string '{search_string}'.")
            return []

        # Build a list of instances of Product using the data retrieved from the database
        products = [Product(**product) for product in product_data]
        
        # Return the list of products
        get_logger().write(TAG, f"Found {len(products)} products for search string '{search_string}'.")
        return products
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Query to get products by search string '{search_string}' failed with error: {e}.")
        raise HTTPException(status_code=500, detail=f"Failed to get products by search string '{search_string}'.")
    finally:
        # Close the MongoDB connection
        client.close()

async def sort_product(criteria: str, price: float = None, asc: bool = True) -> List[Product]:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        collection = db["Products"]
        
        # Define sorting order
        sort_order = 1 if asc else -1

        # Define sorting criteria and query filter in a more compact way
        query_filter = {"price": {"$lte": price}} if criteria == "price" and price is not None else {}
        sort_criteria = [("price", sort_order)] if criteria == "price" else [("title", sort_order)]
        
        # Query to sort products by criteria and order
        get_logger().write(TAG, f"Query to sort products by criteria '{criteria}' in {'ascending' if asc else 'descending'} order executing.")
        product_data = list(collection.find(query_filter).sort(sort_criteria))

        # Check if Products were found
        if not product_data:
            get_logger().write(TAG, f"No Products found for sorting criteria '{criteria}' in {'ascending' if asc else 'descending'} order.")
            return []

        # Build a list of instances of Product using the data retrieved from the database
        products = [Product(**product) for product in product_data]
        
        # Return the list of sorted products
        get_logger().write(TAG, f"Sorted {len(products)} products by criteria '{criteria}' in {'ascending' if asc else 'descending'} order.")
        return products
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Query to sort products by criteria '{criteria}' in {'ascending' if asc else 'descending'} order failed with error: {e}.")
        raise HTTPException(status_code=500, detail=f"Failed to sort products by criteria '{criteria}' in {'ascending' if asc else 'descending'} order.")
    finally:
        # Close the MongoDB connection
        client.close()

async def filter_product(category: str = None, search_string: str = None, criteria: str = None, price: float = None, asc: bool = True) -> List[Product]:
    products = []

    # Filter by category if specified
    if category:
        get_logger().write(TAG, f"Filtering products by category '{category}'")
        products = await get_product_by_category(category)

    # Filter by search string if specified
    if search_string:
        get_logger().write(TAG, f"Filtering products by search string '{search_string}'")
        search_results = await get_product_by_search(search_string)
        if products:
            # Intersect the two lists based on product uid
            products_uids = {product._id for product in products}
            products = [product for product in search_results if product._id in products_uids]
        else:
            products = search_results

    # Eliminate duplicates
    unique_products = {product._id: product for product in products}.values()

    # Sort products if a sorting criterion is specified
    if criteria:
        get_logger().write(TAG, f"Sorting products by criteria '{criteria}'")
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
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Products
        collection = db["Products"]
        
        # Check if the product already exists
        existing_product = collection.find_one({"uid": product_data._id})
        if existing_product:
            get_logger().write(TAG, f"Insert product with uid: {product_data._id} failed, product already exists.")
            raise HTTPException(status_code=400, detail="Product already exists")
        
        # Insert one new product data into the collection
        result = collection.insert_one(product_data.model_dump())
        
        # Return success message
        get_logger().write(TAG, "Product data insert successfully.")
        return "Product inserted successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Failed to insert product data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to insert product data.")
    finally:
        # Close the MongoDB connection
        client.close()

async def delete_product(product_id: str) -> str:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Products
        collection = db["Products"]
        
        # Delete product data from the collection
        get_logger().write(TAG, f"Deleting product data with uid: {product_id} from the database.")
        result = collection.delete_one({"uid": product_id})
        
        # Check if product was found and deleted
        if result.deleted_count == 0:
            get_logger().write(TAG, f"Delete existing product with uid: {product_id} failed, product not found.")
            raise HTTPException(status_code=404, detail="Product not found")

        # Return success message
        get_logger().write(TAG, "Product data deleted successfully.")
        return "Product deleted successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Failed to delete product data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to delete product data.")
    finally:
        # Close the MongoDB connection
        client.close()

async def update_product(product_data: Product) -> str:
    get_logger().write(TAG, f"Connect to the database {DB_NAME} by URI {URI}.")
    client, db = connect_to_database(DB_NAME, URI)
    try:
        # Collection Products
        collection = db["Products"]
        
        # Update product data in the collection
        get_logger().write(TAG, f"Updating product data with uid: {product_data._id} in the database.")
        result = collection.update_one({"uid": product_data._id}, {"$set": product_data.model_dump()})
        
        # Check if product was found and updated
        if result.matched_count == 0:
            get_logger().write(TAG, f"Updating existing product with uid: {product_data._id} failed, product not found.")
            raise HTTPException(status_code=404, detail="Product not found")

        # Return success message
        get_logger().write(TAG, "Product data updated successfully.")
        return "Product updated successfully."
    
    except Exception as e:
        # Other unexpected events occurred
        get_logger().write(TAG, f"Failed to update product data with error: {e}.")
        raise HTTPException(status_code=500, detail="Failed to update product data.")
    finally:
        # Close the MongoDB connection
        client.close()