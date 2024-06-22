# FastAPI
from fastapi import FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import JSONResponse
import uvicorn

# Security & Middleware
from fastapi.security import *
from fastapi.middleware.cors import CORSMiddleware

# Utils
import os
import sys
import signal

from utils.logger import get_logger
from utils.database import *
from models import *
from mongo import *

###################################################################################################

# To Run: uvicorn server:app --host 127.0.0.1 --port 8080 --reload
# To Run: uvicorn server:app --host 127.0.0.1 --port 8080

LOG_SYS = get_logger()
TAG = "FastAPI"

app = FastAPI(title="FastAPI - WTFunko",
              description="A simple and fast api suite for WTFunko e-commerce.",
              summary="Some easy API for WTFunko Store.",
              contact={
                  "email": "antonio.garofalo125@gmail.com",
                  "name": "Antonio Garofalo",
                  "url": "https://github.com/Endless077"
              },
              terms_of_service="http://example.com/terms/",
              license_info={
                  "identifier": "GNU",
                  "name": "GNU General Public License v3",
                  "url": "https://opensource.org/license/gpl-3-0/"
              },
              version="1.0"
              )

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:27017",
    "http://localhost",
    "http://localhost:5173",
    "http://localhost27017"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

###################################################################################################

TAG_USERS = ["Users"]

@app.post("/login", status_code=200, response_model=UserInfo, tags=TAG_USERS,
          summary="User Login",
          description="Authenticate a user with a username and password, returning user information upon successful login.")
async def login(user: User):
    try:
        LOG_SYS.write(TAG, f"Login user with username: {user.username} and password: {user.password}.")
        user_data = await get_user(user.username)

        if hash_string_match(user.password, user_data.password):
            return user_data
        else:
            raise HTTPException(status_code=401, detail="User password don't match")

    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/signup", status_code=201, tags=TAG_USERS,
          summary="User Signup",
          description="Create a new user account with the provided details.")
async def signup(user: User):
    try:
        LOG_SYS.write(TAG, f"Signup user with username: {user.username} and email: {user.email}")
        return await insert_user(user)
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getUser", status_code=200, response_model=User, tags=TAG_USERS,
         summary="Get User Information",
         description="Retrieve user information by username or email.")
async def getUser(username: str = Query(..., description="The username of the user to retrieve."),
                  email: str = Query(None, description="The email of the user to retrieve. If not provided, the user will be retrieved by username.")):
    try:
        LOG_SYS.write(TAG, f"Getting user information with username: {username} or email: {email}.")
        user_data = await get_user(username, email)
        return user_data
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/insertUser", status_code=201, tags=TAG_USERS,
          summary="Insert New User",
          description="Insert a new user into the database with the provided information.")
async def insertUser(user: User):
    try:
        LOG_SYS.write(TAG, f"Insert new user information with username: {user.username}.")
        result = await insert_user(user)
        return {"message": result}
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/deleteUser/{username}", status_code=200, tags=TAG_USERS,
            summary="Delete User",
            description="Delete a user from the database by username.")
async def delete_existing_user(username: str):
    try:
        LOG_SYS.write(TAG, f"Delete existing user information with username: {username}.")
        result = await delete_user(username)
        return {"message": result}
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/updateUser", status_code=200, tags=TAG_USERS,
         summary="Update User Information",
         description="Update the information of a specific user by username.")
async def updateUser(username: str, user: User):
    try:
        LOG_SYS.write(TAG, f"Update existing user information with username: {username}.")
        result = await update_user(username, user)
        return {"message": result}
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


###################################################################################################

TAG_ORDERS = ["Orders"]

@app.get("/getUserOrders", status_code=200, response_model=List[Order], tags=TAG_ORDERS,
         summary="Get User Orders",
         description="Retrieve all orders associated with a user's account by username.")
async def getUserOrders(username: str = Query(..., description="The username of the user whose orders you want to retrieve.")):
    try:
        LOG_SYS.write(TAG, f"Getting all orders information from user account with username: {username}.")
        orders = await get_orders(username)
        return orders
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getOrderInfo", status_code=200, response_model=Order, tags=TAG_ORDERS,
         summary="Get Order Information",
         description="Retrieve the details of a specific order by order ID.")
async def getOrderInfo(order_id: str = Query(..., description="The ID of the order you want to retrieve.")):
    try:
        LOG_SYS.write(TAG, f"Getting all information of a specific order with id: {order_id}.")
        order_info = await get_order_info(order_id)
        return order_info
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/insertOrder", status_code=201, tags=TAG_ORDERS,
          summary="Insert New Order",
          description="Insert a new order into the database with the provided details.")
async def insertOrder(order: Order):
    try:
        LOG_SYS.write(TAG, f"Insert new order information by user:{order.user.username}.")
        result = await insert_order(order)
        return {"message": result}
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/deleteOrder/{order_id}", status_code=200, tags=TAG_ORDERS,
            summary="Delete Order",
            description="Delete a specific order from the database by order ID.")
async def deleteOrder(order_id: str):
    try:
        LOG_SYS.write(TAG, f"Delete existing order information with id: {order_id}.")
        result = await delete_order(order_id)
        return {"message": result}
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/updateOrder", status_code=200, tags=TAG_ORDERS,
         summary="Update Order Information",
         description="Update the information of a specific order by order ID.")
async def updateOrder(order_id: str, order: Order):
    try:
        LOG_SYS.write(TAG, f"Update existing order information with id: {order_id}.")
        result = await update_order(order_id, order)
        return {"message": result}
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

###################################################################################################

TAG_PRODUCTS = ["Products"]


@app.get("/getProducts", response_model=List[Product], status_code=200, tags=TAG_PRODUCTS,
         summary="Get Products",
         description="Retrieve products based on category, search term, sorting criteria, and page index.")
async def getProducts(category: str = Query(..., description="The category of the products to retrieve."),
                      searchTerm: str = Query(..., description="The search term to filter the products."),
                      sortingCriteria: Criteria = Query(..., description="The criteria to sort the products."),
                      pageIndex: int = Query(..., description="The page index to retrieve the products from.")):
    try:
        LOG_SYS.write(TAG, f"Getting products data with some filters at page index {pageIndex}.")
        products = await get_products(category, searchTerm, sortingCriteria, pageIndex)
        return products
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getAllProducts", response_model=List[Product], status_code=200, tags=TAG_PRODUCTS,
         summary="Get All Products",
         description="Retrieve all products available in the database.")
async def getAllProducts():
    try:
        LOG_SYS.write(TAG, f"Getting all product from Database.")
        products = await get_all_products()
        return products
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getUniqueProductsCount", status_code=200, tags=TAG_PRODUCTS,
         summary="Get Unique Products Count",
         description="Retrieve the count of unique products for a specific category and search term.")
async def getUniqueProductsCount(category: str = Query(..., description="The category of the products to count."),
                                 searchTerm: str = Query(..., description="The search term to filter the products.")):
    try:
        LOG_SYS.write(TAG, f"Getting products count with category: {category} and search string: {searchTerm}.")
        count = await get_unique_products_count(category, searchTerm)
        return count
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getByID/{product_id}", response_model=Product, status_code=200, tags=TAG_PRODUCTS,
         summary="Get Product by ID",
         description="Retrieve a specific product by its unique identifier.")
async def getByID(product_id: int):
    try:
        LOG_SYS.write(TAG, f"Getting specific product by id: {product_id}.")
        products = await get_product_by_id(product_id)
        return products
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getByCategory/{category}", response_model=List[Product], status_code=200, tags=TAG_PRODUCTS,
         summary="Get Products by Category",
         description="Retrieve products based on a specific category.")
async def getByCategory(category: str):
    try:
        LOG_SYS.write(TAG, f"Getting products by search category: {category}.")
        products = await get_products_by_category(category)
        return products
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getByProductType/{product_type}", response_model=List[Product], status_code=200, tags=TAG_PRODUCTS,
         summary="Get Products by Product Type",
         description="Retrieve products based on a specific product type.")
async def getBySearch(product_type: str):
    try:
        LOG_SYS.write(
            TAG, f"Getting products by product type: {product_type}.")
        products = await get_product_by_product_type(product_type)
        return products
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getBySearch/{search_string}", response_model=List[Product], status_code=200, tags=TAG_PRODUCTS,
         summary="Get Products by Search String",
         description="Retrieve products based on a specific search string.")
async def getBySearch(search_string: str):
    try:
        LOG_SYS.write(
            TAG, f"Getting products by search string: {search_string}.")
        products = await get_product_by_search(search_string)
        return products
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sortingBy/{criteria}", response_model=List[Product], status_code=200, tags=TAG_PRODUCTS,
         summary="Sort Products",
         description="Sort products based on a specified criteria and order.")
async def sortingBy(criteria: str, asc: bool):
    try:
        LOG_SYS.write(
            TAG, f"Sort products by a specific criteria: {criteria} and by asc: {asc}.")
        products = await sort_product(criteria, asc)
        return products
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getFilter", response_model=List[Product], status_code=200, tags=TAG_PRODUCTS,
         summary="Filter Products",
         description="Filter products based on optional category, search string, and criteria.")
async def getFilter(category: str = None, search_string: str = None, criteria: str = None):
    try:
        LOG_SYS.write(TAG, f"Getting products by combo filter.")
        products = await filter_product(category, search_string, criteria)
        return products
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/insertProduct", status_code=201, tags=TAG_PRODUCTS,
          summary="Insert Product",
          description="Insert a new product into the database.")
async def insertProduct(product: Product):
    try:
        LOG_SYS.write(
            TAG, f"Insert new product information with id: {product._id}.")
        result = await insert_product(product)
        return {"message": result}
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/deleteProduct/{product_id}", status_code=200, tags=TAG_PRODUCTS,
            summary="Delete Product",
            description="Delete a specific product from the database by its identifier.")
async def deleteProduct(product_id: str):
    try:
        LOG_SYS.write(
            TAG, f"Delete existing product information with id: {product_id}.")
        result = await delete_product(product_id)
        return {"message": result}
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.put("/updateProduct/{product_id}", status_code=200, tags=TAG_PRODUCTS,
         summary="Update Product",
         description="Update information of a specific product in the database by its identifier.")
async def updateProduct(product_id: str, product: Product):
    try:
        LOG_SYS.write(
            TAG, f"Update existing product information with id: {product_id}.")
        result = await update_product(product_id, product)
        return {"message": result}
    except HTTPException as http_err:
        LOG_SYS.write(TAG, f"An HTTP error occurred with Exception: {http_err.detail}")
        raise http_err
    except Exception as e:
        LOG_SYS.write(TAG, f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

###################################################################################################

@app.get('/', status_code=200, tags=["root"])
@app.get('/about', status_code=200, tags=["root"])
async def about():
    return {"App Name": "WTFunko"}

###################################################################################################

STARTUP_TAG = "STARTUP"


def welcome_message():
    LOG_SYS.write(STARTUP_TAG, "__          _________ ______           _          ")
    LOG_SYS.write(STARTUP_TAG, "\ \        / /__   __|  ____|         | |         ")
    LOG_SYS.write(STARTUP_TAG, " \ \  /\  / /   | |  | |__ _   _ _ __ | | _____   ")
    LOG_SYS.write(STARTUP_TAG, "  \ \/  \/ /    | |  |  __| | | | '_ \| |/ / _ \  ")
    LOG_SYS.write(STARTUP_TAG, "   \  /\  /     | |  | |  | |_| | | | |   < (_) | ")
    LOG_SYS.write(STARTUP_TAG, "    \/  \/      |_|  |_|   \__,_|_| |_|_|\_\___/  ")

SHUTDOWN_TAG = "SHUTDOWN"

def shutdown(signum, frame):
    try:
        LOG_SYS.write(SHUTDOWN_TAG, "Closing Database MongoDB connection.")
        close_connection()
        LOG_SYS.write(SHUTDOWN_TAG, "Shutdown FastAPI server.")
        sys.exit(0)
    except Exception as e:
        LOG_SYS.write(SHUTDOWN_TAG, f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    # Call Signal Registration
    signal.signal(signal.SIGINT, shutdown)   # Ctrl+C
    signal.signal(signal.SIGTERM, shutdown)  # kill
    signal.signal(signal.SIGHUP, shutdown)   # Terminal closed
    signal.signal(signal.SIGQUIT, shutdown)  # Quit signal
    signal.signal(signal.SIGABRT, shutdown)  # Abort signal
    signal.signal(signal.SIGUSR1, shutdown)  # User-defined signal 1
    signal.signal(signal.SIGUSR2, shutdown)  # User-defined signal 2

    welcome_message()

    # Connect to MongoDB
    connect(host="localhost", port=27017, db_name="WTFunko")

    # Start Uvicorn App
    uvicorn.run(app, host="localhost", port=8000)
