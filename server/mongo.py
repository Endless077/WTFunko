from fastapi import HTTPException

import pymongo
import pymongo.collection

from utils.logger import get_logger
from utils.database import get_database

from mongo import *
from models import *
from utils.utils import *
from utils.enumerations.criteria import *

import math

LOG_SYS = get_logger()
DATABASE = None
AMOUNT_PRODUCT_PAGE = 20

TAG = "MongoDB"

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


def create_product_indices(products: pymongo.collection.Collection):
    products.create_index([("interest", 1)])
    products.create_index([("product_type", 1)])
    products.create_index([("title", 1)])
    products.create_index([("price", 1)])


def populate_database():
    try:
        dataset_path = "../source/json/"
        populate_users(dataset_path)
        populate_orders(dataset_path)
        populate_products(dataset_path)
    except pymongo.errors.PyMongoError as e:
        LOG_SYS.write(TAG, f"An error occurred with MongoDB: {e}")
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")


def populate_users(dataset_path):
    users_dataset_path = dataset_path + "users.json"
    users_dataset = list(read_json(users_dataset_path).values())
    users = DATABASE["Users"]
    count = users.count_documents({})
    if count > 0:
        LOG_SYS.write(TAG, "A collection for users already exists.")
    else:
        result = users.insert_many(users_dataset)
        LOG_SYS.write(TAG, f"Filled the users collection with {len(result.inserted_ids)} documents.")


def populate_orders(dataset_path):
    orders_dataset_path = dataset_path + "orders.json"
    orders_dataset = list(read_json(orders_dataset_path).values())
    orders = DATABASE["Orders"]
    count = orders.count_documents({})
    if count > 0:
        LOG_SYS.write(TAG, "A collection for orders already exists.")
    else:
        result = orders.insert_many(orders_dataset)
        LOG_SYS.write(TAG, f"Filled the orders collection with {len(result.inserted_ids)} documents.")


def populate_products(dataset_path):
    products_dataset_path = dataset_path + "products.json"
    products_dataset = list(read_json(products_dataset_path).values())
    products = DATABASE["Products"]
    count = products.count_documents({})
    if count > 0:
        LOG_SYS.write(TAG, "A collection for products already exists.")
    else:
        result = products.insert_many(products_dataset)
        create_product_indices(products)
        LOG_SYS.write(TAG, f"Filled the funko pops collection with {len(result.inserted_ids)} documents.")


async def get_all_users():
    collection = DATABASE["Users"]
    LOG_SYS.write(TAG, "Query to get all users executing.")
    users_data = list(collection.find())
    if not users_data:
        LOG_SYS.write(TAG, "No Users found.")
        return []
    
    # Build a list of instances of User using the data retrieved from the database
    users = [User(**user) for user in users_data]
    LOG_SYS.write(TAG, f"Found {len(users_data)} users.")
    return users


async def get_user(username: str, email: str = None) -> User:
    collection = DATABASE["Users"]
    # Query to find the user in the collection by username or password
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


async def insert_user(user_data: User, generate_uid: bool = True) -> str:
    collection = DATABASE["Users"]
    existing_user_username = collection.find_one({"username": user_data.username})
    if existing_user_username:
        LOG_SYS.write(TAG, f"Insert new user with username: {user_data.username} failed, user already exists.")
        raise HTTPException(status_code=400, detail="User already exists")

    # Insert user with custom or random UID
    if not generate_uid:
        # Check if the user already exists (if true rise exeption)
        existing_user_id = collection.find_one({"_id": user_data.id})
        if existing_user_id:
            LOG_SYS.write(TAG, f"Insert user with id: {user_data.id} failed, user already exists.")
            raise HTTPException(
                status_code=400, detail="User already exists")
    else:
        while (True):
            # Generate a UID string for the user
            user_data.id = generate_unique_id(length=13, alphanumeric=True)
            existing_user_id = collection.find_one({"_id": user_data.id})
            if not existing_user_id:
                break

    # Hashing the user password in bcrypt hash algorithm
    user_data.password = hash_string(user_data.password)
    collection.insert_one(user_data.model_dump(by_alias=True))
    LOG_SYS.write(TAG, "User data insert successfully.")
    return user_data


async def delete_user(username: str) -> str:
    collection = DATABASE["Users"]
    LOG_SYS.write(TAG, f"Deleting user with username: {username} from the database.")
    result = collection.delete_one({"username": username})
    LOG_SYS.write(TAG, f"Deleted {result.deleted_count} documents in the User collection.")
    LOG_SYS.write(TAG, "User data deleted successfully.")
    return f"User {username} deletion successfully."


async def clear_users() -> str:
    collection = DATABASE["Users"]
    collection.delete_many({})
    LOG_SYS.write(TAG, "All Users data deleted successfully.")
    return "Users collection cleared successfully."


async def update_user(username: str, user_data: Optional[Union[User, Dict[str, Any]]]) -> str:
    collection = DATABASE["Users"]
    # Update user data from the collection
    newUserData = user_data.model_dump() if isinstance(user_data, User) else user_data
    LOG_SYS.write(TAG, f"Updating product data with id: {username} in the datbase.")
    result = collection.update_one({"username": username}, {"$set": newUserData})
    # Check if user was found and updated
    if result.matched_count == 0:
        LOG_SYS.write(TAG, f"Updating existing user with username: {username} failed, user not found.")
        raise HTTPException(status_code=404, detail="User not found")

    LOG_SYS.write(TAG, "User data updated successfully.")
    return f"User {username} updated successfully."


async def get_all_orders():
    collection = DATABASE["Orders"]
    LOG_SYS.write(TAG, "Query to get all users executing.")
    orders_data = list(collection.find())
    if not orders_data:
        LOG_SYS.write(TAG, "No Orders found.")
        return []

    # Build a list of instances of Order using the data retrieved from the database
    users = [Order(**order) for order in orders_data]
    LOG_SYS.write(TAG, f"Found {len(orders_data)} orders.")
    return users


async def get_orders_by_username(username: str) -> List[Order]:
    collection = DATABASE["Orders"]
    # Query to find user orders in the collection by username and sort by date in descending order
    LOG_SYS.write(TAG, f"Query to get orders for username: {username} executing.")
    orders_data = list(collection.find({"user.username": username}).sort("date", -1))
    if not orders_data:
        LOG_SYS.write(TAG, f"No orders found for username: {username}.")
        raise HTTPException(status_code=404, detail="Orders not found.")

    # Build a list of instance of Orders using the data retrieved from the database
    orders = [Order(**order) for order in orders_data]
    LOG_SYS.write(TAG, f"Found {len(orders)} orders for user: {username}")
    return orders


async def get_order_info(order_id: str) -> Order:
    collection = DATABASE["Orders"]
    # Query to find order info in the collection byid
    LOG_SYS.write(TAG, f"Query to get order info forid: {order_id} executing.")
    order_data = collection.find_one({"_id": order_id})
    if order_data is None:
        LOG_SYS.write(TAG, f"Order with ID: {order_id} not found.")
        raise HTTPException(status_code=404, detail="Order not found.")

    # Build an instance of Order using the data retrieved from the database
    order = Order(**order_data)
    return order


async def insert_order(order_data: Order, generate_uid: bool = True) -> str:
    collection = DATABASE["Orders"]
    # Insert order with custom or random UID
    if not generate_uid:
        existing_order = collection.find_one({"_id": order_data.id})
        if existing_order:
            LOG_SYS.write(TAG, f"Insert order with id: {order_data.id} failed, order already exists.")
            raise HTTPException(
                status_code=400, detail="Order already exists")
    else:
        while (True):
            # Generate a UID string for the order
            order_data.id = generate_unique_id(length=13, alphanumeric=True)
            # Check if order already exist (if false break the while)
            existing_order = collection.find_one({"_id": order_data.id})
            if not existing_order:
                break

    # Insert one new order data into database
    collection.insert_one(order_data.model_dump(by_alias=True))
    LOG_SYS.write(TAG, "Order data insert successfully.")
    return f"Order {order_data.id} by user {order_data.user.username} inserted successfully."


async def delete_order_by_id(order_id: str) -> str:
    collection = DATABASE["Orders"]
    LOG_SYS.write(TAG, f"Deleting order data with id: {order_id} from the database.")
    result = collection.delete_one({"_id": order_id})
    LOG_SYS.write(TAG, f"Deleted {result.deleted_count} documents in the Orders collection.")
    LOG_SYS.write(TAG, "Order data deleted successfully.")
    return f"Order {order_id} deleted successfully."


async def delete_orders_by_username(username: str) -> str:
    collection = DATABASE["Orders"]
    LOG_SYS.write(TAG, f"Deleting order data with username: {username} from the database.")
    result = collection.delete_many({"user.username": username})
    LOG_SYS.write(TAG, f"Deleted {result.deleted_count} documents in the Orders collection.")
    LOG_SYS.write(TAG, "Order data deleted successfully.")
    return f"All order created by {username} deleted successfully."


async def clear_orders() -> str:
    collection = DATABASE["Orders"]
    collection.delete_many({})
    LOG_SYS.write(TAG, "All Orders data deleted successfully.")
    return "Orders collection cleared successfully."


async def update_order(order_id: str, order_data: Optional[Union[Order, Dict[str, Any]]]) -> str:
    collection = DATABASE["Orders"]
    # Update order data in the collection
    newOrderData = order_data.model_dump() if isinstance(order_data, Product) else order_data
    LOG_SYS.write(TAG, f"Updating product data with id: {order_id} in the datbase.")
    result = collection.update_one({"_id": order_id}, {"$set": newOrderData})
    # Check if order was found and updated
    if result.matched_count == 0:
        LOG_SYS.write(TAG, f"Updating existing order with id: {order_id} failed, order not found.")
        raise HTTPException(status_code=404, detail="Order not found")

    LOG_SYS.write(TAG, "Order data updated successfully.")
    return f"Order {order_id} updated successfully."


async def get_unique_products_count(category: str, searchTerm: str) -> int:
    collection = DATABASE["Products"]
    # Getting cutom filter and count occurrence
    filter = getCombinedFilter(category, searchTerm)
    count = collection.count_documents(filter)
    return count


def getCombinedFilter(category: str, searchTerm: str) -> dict:
    # Create a combofilter between all possible filters
    category_filter = {} if category.lower() == "all" else {
        "interest": {"$in": [category]}}
    search_filter = {
        "$or": [
            {"title": {"$regex": searchTerm, "$options": "i"}},
            {"description": {"$regex": searchTerm, "$options": "i"}},
            {"product_type": {"$regex": searchTerm, "$options": "i"}}
        ]
    }

    combined_filters = {"$and": [category_filter, search_filter]}
    return combined_filters


async def get_all_products() -> List[Product]:
    collection = DATABASE["Products"]
    LOG_SYS.write(TAG, "Query to get all products executing.")
    products_data = list(collection.find())
    if not products_data:
        LOG_SYS.write(TAG, "No Products found.")
        return []

    # Build a list of instances of Product using the data retrieved from the database
    products = [Product(**product) for product in products_data]
    LOG_SYS.write(TAG, f"Found {len(products)} products.")
    return products


async def get_products(category: str, searchTerm: str, criteria: Criteria, pageIndex: int) -> List[Product]:
    collection = DATABASE["Products"]
    # Get a filter and sorting rule
    LOG_SYS.write(TAG, "Creating a combined custom filter and sorter.")
    filter = getCombinedFilter(category, searchTerm)
    sort = getCriteriaSorting(criteria)
    # Setup max page and range index
    count = await get_unique_products_count(category, searchTerm)
    if count == 0:
        LOG_SYS.write(TAG, "No Products found.")
        return []
    max_pages = math.ceil(count / 20.0)
    if pageIndex < 0 or pageIndex > max_pages - 1:
        raise ValueError("Invalid pages range specified.")

    # Query to find Products info in the collection by pageIndex
    LOG_SYS.write(TAG, "Query to get products pages executing.")
    start_range = pageIndex * AMOUNT_PRODUCT_PAGE
    end_range = min((pageIndex + 1) * AMOUNT_PRODUCT_PAGE, count)
    product_data = list(collection.find(filter).sort(sort).skip(start_range).limit(end_range - start_range))
    if not product_data:
        LOG_SYS.write(TAG, "No Products found.")
        return []

    # Build a list of instances of Product using the data retrieved from the database
    products = [Product(**product) for product in product_data]
    LOG_SYS.write(TAG, f"Found {len(products)} products.")
    return products


async def get_product_by_id(product_id: int) -> Product:
    collection = DATABASE["Products"]
    LOG_SYS.write(TAG, f"Query to get products info for id: {product_id} executing.")
    products_data = collection.find_one({"_id": product_id})
    if products_data is None:
        LOG_SYS.write(TAG, f"Product with id: {product_id} not found.")
        raise HTTPException(status_code=404, detail="Product not found.")

    # Build an instance of Product using the data retrieved from the database
    product = Product(**products_data)
    return product


async def get_products_by_category(category: str) -> List[Product]:
    collection = DATABASE["Products"]
    LOG_SYS.write(TAG, f"Query to get products by category '{category}' executing.")
    # Query to find products by category in the collection
    product_data = list(collection.find({"interest": {"$in": [category]}}))
    if not product_data:
        LOG_SYS.write(TAG, f"No Products found for category '{category}'.")
        return []
    # Build a list of instances of Product using the data retrieved from the database
    products = [Product(**product) for product in product_data]
    LOG_SYS.write(TAG, f"Found {len(products)} products for category '{category}'.")
    return products


async def get_product_by_product_type(product_type: str) -> List[Product]:
    collection = DATABASE["Products"]
    LOG_SYS.write(TAG, f"Query to get products by search string '{product_type}' executing.")
    # Query to find products by search string in the title
    product_data = list(collection.find({"product_type": {"$regex": f".*{product_type}.*", "$options": "i"}}))
    if not product_data:
        LOG_SYS.write(TAG, f"No Products found for product type: '{product_type}'.")
        return []

    # Build a list of instances of Product using the data retrieved from the database
    products = [Product(**product) for product in product_data]
    LOG_SYS.write(TAG, f"Found {len(products)} products for product type '{product_type}'.")
    return products


async def get_product_by_search(search_string: str) -> List[Product]:
    collection = DATABASE["Products"]
    
    # Query to find products by search string in the title
    LOG_SYS.write(TAG, f"Query to get products by search string '{search_string}' executing.")
    product_data = list(collection.find({
        "$or": [
            {"title": {"$regex": search_string, "$options": "i"}},
            {"description": {"$regex": search_string, "$options": "i"}},
            {"product_type": {"$regex": search_string, "$options": "i"}}
        ]
    }))
    if not product_data:
        LOG_SYS.write(TAG, f"No Products found for search string '{search_string}'.")
        return []

    # Build a list of instances of Product using the data retrieved from the database
    products = [Product(**product) for product in product_data]
    LOG_SYS.write(TAG, f"Found {len(products)} products for search string '{search_string}'.")
    return products


async def sort_product_by_price(price: float = None, asc: bool = True) -> List[Product]:
    collection = DATABASE["Products"]
    sort_order = 1 if asc else -1
    # Define sorting criteria and query filter in a more compact way
    query_filter = ({"price": {"$lte": price}})
    sort_criteria = ([("price", sort_order)])
    # Query to sort products by criteria and order
    LOG_SYS.write(TAG, f"Query to sort products by price in {'ascending' if asc else 'descending'} order executing.")
    product_data = list(collection.find(query_filter).sort(sort_criteria))
    if not product_data:
        LOG_SYS.write(TAG, f"No Products found for sorting by price in {'ascending' if asc else 'descending'} order.")
        return []

    # Build a list of instances of Product using the data retrieved from the database
    products = [Product(**product) for product in product_data]
    LOG_SYS.write(TAG, f"Sorted {len(products)} products by price in {'ascending' if asc else 'descending'} order.")
    return products


async def sort_product_by_name(asc: bool = True) -> List[Product]:
    collection = DATABASE["Products"]
    sort_order = 1 if asc else -1
    # Define sorting criteria and query filter in a more compact way
    sort_criteria = ([("title", sort_order)])
    # Query to sort products by criteria and order
    LOG_SYS.write(TAG, f"Query to sort products by price in {'ascending' if asc else 'descending'} order executing.")
    product_data = list(collection.find().sort(sort_criteria))
    if not product_data:
        LOG_SYS.write(TAG, f"No Products found for sorting by price in {'ascending' if asc else 'descending'} order.")
        return []

    # Build a list of instances of Product using the data retrieved from the database
    products = [Product(**product) for product in product_data]
    LOG_SYS.write(TAG, f"Sorted {len(products)} products by price in {'ascending' if asc else 'descending'} order.")
    return products


async def insert_product(product_data: Product, generate_uid: bool = True) -> str:
    collection = DATABASE["Products"]
    # Insert product with custom or random UID
    if not generate_uid:
        existing_product = collection.find_one({"_id": product_data.id})
        if existing_product:
            LOG_SYS.write(    TAG, f"Insert product with id: {product_data.id} failed, product already exists.")
            raise HTTPException(
                status_code=400, detail="Product already exists")
    else:
        while (True):
            # Generate a UID string for the product
            product_data.id = generate_unique_id(length=13, alphanumeric=False)
            existing_product = collection.find_one({"_id": product_data.id})
            if not existing_product:
                break

    # Insert one new product data into database
    collection.insert_one(product_data.model_dump(by_alias=True))
    LOG_SYS.write(TAG, "Product data insert successfully.")
    return f"Product {product_data.id} inserted successfully."


async def delete_product(product_id: int) -> str:
    collection = DATABASE["Products"]
    LOG_SYS.write(TAG, f"Deleting product data with id: {product_id} from the database.")
    result = collection.delete_one({"_id": product_id})
    LOG_SYS.write(TAG, f"Deleted {result.deleted_count} documents in the Products collection.")
    LOG_SYS.write(TAG, "Product data deleted successfully.")
    return f"Product {product_id} deleted successfully."


async def clear_products() -> str:
    collection = DATABASE["Products"]
    collection.delete_many({})
    LOG_SYS.write(TAG, "All Products data deleted successfully.")
    return "Products collection cleared successfully."


async def update_product_warehouse(products: List[Optional[Union[OrderProduct, Dict[str, Any]]]]):
    collection = DATABASE["Products"]
    # Update product quantity in the collection
    for product in products:
        LOG_SYS.write(TAG, f"Updateing {product.id} stock in the warehouse.")
        amount_value = product.amount
        quantity_value = collection.find_one({"_id": product.id}, {"quantity": 1}).get("quantity", 0)
        restock = max(quantity_value - amount_value, 0)
        await update_product(product.id, {"quantity": restock})
      
    return "All quantity product in the warehouse are updated."


async def update_product(product_id: int, product_data: Optional[Union[Product, Dict[str, Any]]]) -> str:
    collection = DATABASE["Products"]
    # Update product data in the collection
    newProductData = product_data.model_dump() if isinstance(product_data, Product) else product_data
    LOG_SYS.write(TAG, f"Updating product data with id: {product_id} in the datbase.")
    result = collection.update_one({"_id": product_id}, {"$set": newProductData})
    if result.matched_count == 0:
        LOG_SYS.write(TAG, f"Updating existing product with id: {product_id} failed, product not found.")
        raise HTTPException(status_code=404, detail="Product not found")

    LOG_SYS.write(TAG, "Product data updated successfully.")
    return f"Product {product_id} updated successfully."