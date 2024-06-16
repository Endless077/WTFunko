# FastAPI
from fastapi import HTTPException

# MongoDB
import pymongo

# Own Models
from utils.logger import get_logger
from utils.database import get_database

from mongo import *
from models import *
from utils.utils import *

# Utils
import math

LOG_SYS = get_logger()
DATABASE = None

TAG = "MongoDB"

###################################################################################################


def connect(host="localhost", port=27017, db_name=None, username=None, password=None):
    global DATABASE

    if username is None or password is None:
        URI = f"mongodb://{host}:{port}/{db_name}"
    else:
        URI = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
    try:
        LOG_SYS.write(TAG, "Connection to MongoDB.")
        DATABASE = get_database(URI, db_name)
        LOG_SYS.write(TAG, "Population of the database.")
        populate_database()
    except Exception as e:
        LOG_SYS.write(TAG, f"Error connecting to MongoDB: {e}")


def populate_database():
    try:
        dataset_path = "../source/json/"
        users_dataset_path = dataset_path + "users.json"
        orders_dataset_path = dataset_path + "orders.json"
        products_dataset_path = dataset_path + "products.json"

        users_dataset = list(read_json(users_dataset_path).values())
        orders_dataset = list(read_json(orders_dataset_path).values())
        products_dataset = list(read_json(products_dataset_path).values())

        users = DATABASE["Users"]
        count = users.count_documents({})
        if count > 0:
            LOG_SYS.write(TAG, "A collection for users already exists.")
        else:
            result = users.insert_many(users_dataset)
            LOG_SYS.write(TAG, f"Filled the users collection with {len(result.inserted_ids)} documents.")

        orders = DATABASE["Orders"]
        count = orders.count_documents({})
        if count > 0:
            LOG_SYS.write(TAG, "A collection for orders already exists.")
        else:
            result = orders.insert_many(orders_dataset)
            LOG_SYS.write(TAG, f"Filled the orders collection with {len(result.inserted_ids)} documents.")

        products = DATABASE["Products"]
        count = products.count_documents({})
        if count > 0:
            LOG_SYS.write(TAG, "A collection for products already exists.")
        else:
            result = products.insert_many(products_dataset)
            LOG_SYS.write(TAG, f"Filled the funko pops collection with {len(result.inserted_ids)} documents.")

    except pymongo.errors.PyMongoError as e:
        LOG_SYS.write(TAG, f"An error occurred with MongoDB: {e}")
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")


###################################################################################################


async def get_user(username: str, email: str = None) -> User:
    collection = DATABASE["Users"]
    # Execute the query to find the user in the collection by username or password
    LOG_SYS.write(TAG, f"Query to get user information by username: {username} or email: {email} executing.")
    query = {"username": username}
    if email is not None:
        query = {"$or": [{"username": username}, {"email": email}]}
    user_data = collection.find_one(query)

    # If the user is not found in the database, raise an exception
    if user_data is None:
        LOG_SYS.write(TAG, f"Query to get user information by username: {username} or email: {email} failed, user not found.")
        raise HTTPException(status_code=404, detail="User not found.")

    # Build an instance of User using the data retrieved from the database
    LOG_SYS.write(TAG, f"Query to get user information by username: {username} or email: {email} success.")
    user = User(**user_data)
    return user


async def insert_user(user_data: User) -> str:
    # Collection Users
    collection = DATABASE["Users"]

    # Check if the user already exists
    existing_user = collection.find_one({"username": user_data.username})
    if existing_user:
        LOG_SYS.write(TAG, f"Insert new user with username: {user_data.username} failed, user already exists.")
        raise HTTPException(status_code=400, detail="User already exists")

    # Insert one new user data into the collection
    user_data.id = generate_unique_id(length=13, string=False)
    user_data.password = hash_string(user_data.password)
    result = collection.insert_one(user_data.model_dump(by_alias=True))

    # Return success message
    LOG_SYS.write(TAG, "User data insert successfully.")
    return "User inserted successfully."


async def delete_user(username: str) -> str:
    # Collection Users
    collection = DATABASE["Users"]

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


async def update_user(user_data: User) -> str:
    # Collection Users
    collection = DATABASE["Users"]

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


###################################################################################################


async def get_orders(username: str) -> List[Order]:
    # Collection Orders
    collection = DATABASE["Orders"]

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


async def get_order_info(order_id: str) -> Order:
    # Collection Orders
    collection = DATABASE["Orders"]

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


async def insert_order(order_data: Order) -> str:
    # Collection Orders
    collection = DATABASE["Orders"]

    # Query to find if order already exist
    existing_order = collection.find_one({"uid": order_data._id})

    # Check if order already exist
    if existing_order:
        LOG_SYS.write(TAG, f"Insert order with uid: {order_data._id} failed, order already exists.")
        raise HTTPException(status_code=400, detail="Order already exists")

    # Insert one new order data into database
    order_data.id = generate_unique_id(length=13, string=False)
    result = collection.insert_one(order_data.model_dump(by_alias=True))

    # Return success message
    LOG_SYS.write(TAG, "Order data insert successfully.")
    return "Order inserted successfully."


async def delete_order(order_id: str) -> str:
    # Collection Orders
    collection = DATABASE["Orders"]

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


async def update_order(order_data: Order) -> str:
    # Collection Orders
    collection = DATABASE["Orders"]

    # Update one funcion to update the new order infos
    LOG_SYS.write(TAG, f"Updating order data with uid: {order_data._id} in the database.")
    result = collection.update_one({"uid": order_data._id}, {"$set": order_data.model_dump()})

    # Check if order was found and updated
    if result.matched_count == 0:
        LOG_SYS.write(TAG, f"Updating existing order with uid: {order_data._id} failed, order not found.")
        raise HTTPException(status_code=404, detail="Order not found")

    # Return success message
    LOG_SYS.write(TAG, "Order data updated successfully.")
    return "Order updated successfully."

###################################################################################################


async def get_all_products() -> List[Product]:
    # Collection Products
    products = DATABASE["Products"]

    # Query to find all Product info in the collection
    LOG_SYS.write(TAG, "Query to get all products executing.")
    product_data = list(products.find())
    if not product_data:
        LOG_SYS.write(TAG, "No Products found.")
        return []

    # Build a list of instances of Product using the data retrieved from the database
    products = [Product(**product) for product in product_data]
    LOG_SYS.write(TAG, f"Found {len(products)} products.")
    return products


async def get_unique_products_count() -> int:
    # Collection Products
    products = DATABASE["Products"]
    
    # Setup max page and range index
    count = products.count_documents({})
    return count


async def get_products_from_page(pageIndex: int) -> List[Product]:
    # Collection Products
    products = DATABASE["Products"]
    
    # Setup max page and range index
    count = products.count_documents({})
    max_pages = math.ceil(count / 20.0)
    if pageIndex < 0 or pageIndex > max_pages - 1:
        raise ValueError("Invalid pages range specified.")

    # Query to find Products info in the collection by pageIndex
    LOG_SYS.write(TAG, "Query to get products pages executing.")
    amountPerPage = 20
    start_range = pageIndex * amountPerPage
    end_range = min((pageIndex + 1) * amountPerPage, count)
    product_data = list(products.find().skip(start_range).limit(end_range - start_range))
    if not product_data:
        LOG_SYS.write(TAG, "No Products found.")
        return []

    # Build a list of instances of Product using the data retrieved from the database
    products = [Product(**product) for product in product_data]
    LOG_SYS.write(TAG, f"Found {len(products)} products.")
    return products


async def get_product(product_id) -> Product:
    # Collection Products
    products = DATABASE["Products"]

    # Query to find Product info in the collection by id
    LOG_SYS.write(TAG, f"Query to get products info for id: {product_id} executing.")
    products_data = products.find_one({"_id": product_id})
    if products_data is None:
        LOG_SYS.write(TAG, f"Product with id: {product_id} not found.")
        raise HTTPException(status_code=404, detail="Product not found.")

    # Build an instance of Product using the data retrieved from the database
    product = Product(**products_data)
    return product


async def get_product_by_category(category: str) -> List[Product]:
    # Collection Products
    collection = DATABASE["Products"]

    # Query to find products by category in the collection
    LOG_SYS.write(
        TAG, f"Query to get products by category '{category}' executing.")
    product_data = list(collection.find({"interest": {"$in": [category]}}))

    # Check if Products were found
    if not product_data:
        LOG_SYS.write(TAG, f"No Products found for category '{category}'.")
        return []

    # Build a list of instances of Product using the data retrieved from the database
    products = [Product(**product) for product in product_data]

    # Return the list of products
    LOG_SYS.write(
        TAG, f"Found {len(products)} products for category '{category}'.")
    return products


async def get_product_by_search(search_string: str) -> List[Product]:
    # Collection Products
    collection = DATABASE["Products"]

    # Query to find products by search string in the title
    LOG_SYS.write(TAG, f"Query to get products by search string '{search_string}' executing.")
    product_data = list(collection.find({"title": {"$regex": f".*{search_string}.*", "$options": "i"}}))

    # Check if Products were found
    if not product_data:
        LOG_SYS.write(
            TAG, f"No Products found for search string '{search_string}'."
        )
        return []

    # Build a list of instances of Product using the data retrieved from the database
    products = [Product(**product) for product in product_data]

    # Return the list of products
    LOG_SYS.write(
        TAG, f"Found {len(products)} products for search string '{search_string}'."
    )
    return products


async def sort_product(criteria: str, price: float = None, asc: bool = True) -> List[Product]:
    collection = DATABASE["Products"]

    # Define sorting order
    sort_order = 1 if asc else -1

    # Define sorting criteria and query filter in a more compact way
    query_filter = (
        {"price": {"$lte": price}}
        if criteria == "price" and price is not None
        else {}
    )
    sort_criteria = ([("price", sort_order)] if criteria == "price" else [("title", sort_order)])

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


async def filter_product(
    category: str = None,
    search_string: str = None,
    criteria: str = None,
    price: float = None,
    asc: bool = True,
) -> List[Product]:
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
            products_uids = {product._id for product in products}
            products = [product for product in search_results if product._id in products_uids]
        else:
            products = search_results

    # Eliminate duplicates
    unique_products = {product._id: product for product in products}.values()

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
                unique_products = sorted(
                    unique_products,
                    key=lambda x: x.price if criteria == "price" else x.title,
                    reverse=not asc,
                )
            else:
                # If there are no previously filtered products, call the sorting function without price
                products = await sort_product(criteria=criteria, asc=asc)

    return list(unique_products)


async def insert_product(product_data: Product) -> str:
    # Collection Products
    collection = DATABASE["Products"]

    # Check if the product already exists
    existing_product = collection.find_one({"uid": product_data._id})
    if existing_product:
        LOG_SYS.write(TAG, f"Insert product with uid: {product_data._id} failed, product already exists.")
        raise HTTPException(
            status_code=400, detail="Product already exists")

    # Insert one new product data into database
    product_data.id = generate_unique_id(length=13, string=False)
    result = collection.insert_one(product_data.model_dump(by_alias=True))

    # Return success message
    LOG_SYS.write(TAG, "Product data insert successfully.")
    return "Product inserted successfully."


async def delete_product(product_id: str) -> str:
    # Collection Products
    collection = DATABASE["Products"]

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


async def update_product(product_data: Product) -> str:
    # Collection Products
    collection = DATABASE["Products"]

    # Update product data in the collection
    LOG_SYS.write(TAG, f"Updating product data with uid: {product_data._id} in the database.")
    result = collection.update_one({"uid": product_data._id}, {"$set": product_data.model_dump()})

    # Check if product was found and updated
    if result.matched_count == 0:
        LOG_SYS.write(TAG, f"Updating existing product with uid: {product_data._id} failed, product not found.")
        raise HTTPException(status_code=404, detail="Product not found")

    # Return success message
    LOG_SYS.write(TAG, "Product data updated successfully.")
    return "Product updated successfully."
