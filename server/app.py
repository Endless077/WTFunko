# FastAPI
from fastapi import FastAPI, HTTPException, Request, Response

# Security & Middleware
from fastapi.security import *
from fastapi.middleware.cors import CORSMiddleware

# Uvicorn
import uvicorn

# Date time
from datetime import datetime as dt

# Utils
import os
import sys
import asyncio
import logging

# Own Modules
# Add the project root directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from utils.logger import get_logger
from utils.database import *
from server.models import *
from server.mongo import *

###################################################################################################

# To Run: uvicorn server:app --host 127.0.0.1 --port 8080 --reload
# To Run: uvicorn server:app --host 127.0.0.1 --port 8080

LOG_SYS = get_logger()
TAG = "FastAPI"

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('pymongo')
log.setLevel(logging.WARNING)

app = FastAPI(title="FastAPI - ML Test Suite",
              description="A simple and fast api suite for a WTFunko e-commerce.",
              summary="Some easy API for WTFunko website.",
              contact={
                "name": "Antonio Garofalo",
                "url": "https://github.com/Endless077",
                "email": "antonio.garofalo125@gmail.com"
                },
              terms_of_service="http://example.com/terms/",
              license_info={
                "identifier": "GNU",
                "name": "GNU General Public License v3",
                "url": "https://opensource.org/license/gpl-3-0/"
                },
              version="1.0"
              )

# TODO: da modificare la CORS.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

###################################################################################################

@app.get("/getUser", status_code=200, response_model=User, description="Get a specific user by username or email.")
async def getUser(username: str, email: str):
    try:
        LOG_SYS.write(TAG, f"Getting user information with username: {username} or email: {email}.")
        user_data = await get_user(username, email)
        return user_data
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An error occured with Excepytion: {e}")
        raise e


@app.post("/insertUser", status_code=201, description="Insert a new user in the database.")
async def insertUser(user: User):
    try:
        LOG_SYS.write(TAG, f"Insert new user information with username: {user.username}.")
        result = await insert_user(user)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/user/{username}", status_code=200, description="Delete a specific user information by username.")
async def delete_existing_user(username: str):
    try:
        LOG_SYS.write(TAG, f"Delete existing user information with username: {username}.")
        result = await delete_user(username)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/updateUser", status_code=200, description="Update a specific user information by username.")
async def updateUser(username: str, user: User):
    try:
        LOG_SYS.write(TAG, f"Update existing user information with username: {username}.")
        result = await update_user(user)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))
      

###################################################################################################

@app.get("/getUserOrders", status_code=200, response_model=List[Order], description="Get all orders from a user account by username.")
async def getUserOrders(username: str):
    try:
        LOG_SYS.write(TAG, f"Getting all orders information from user account with username: {username}.")
        orders = await get_orders(username)
        return orders
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getOrderInfo", status_code=200, response_model=Order, description="Get a specific order infos by id.")
async def getOrderInfo(order_id: str):
    try:
        LOG_SYS.write(TAG, f"Getting all information of a specifc order with id: {order_id}.")
        order_info = await get_order_info(order_id)
        return order_info
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/insertOrder", status_code=201, description="Insert a new order in the database.")
async def insertOrder(order: Order):
    try:
        LOG_SYS.write(TAG, f"Insert new order information with username: {order.order_id}.")
        result = await insert_order(order)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/deleteOrder/{order_id}", status_code=200, description="Delete a specific order information by id.")
async def deleteOrder(order_id: str):
    try:
        LOG_SYS.write(TAG, f"Delete existing order information with id: {order_id}.")
        result = await delete_order(order_id)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


app.put("/updateOrder", status_code=200, description="Update a specific order information by id.")
async def updateOrder(order_id: str, order: Order):
    try:
        LOG_SYS.write(TAG, f"Update existing order information with id: {order_id}.")
        result = await update_order(order)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

###################################################################################################

@app.get("/getAllProducts", response_model=List[Product], status_code=200, description="Get all products.")
async def getAllProducts():
    try:
        LOG_SYS.write(TAG, f"Getting all product from Database.")
        products = await get_all_products()
        return products
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getProduct/{product_id}", response_model=Product, status_code=200, description="Get a specific producs list by id.")
async def getProduct(product_id: int):
    try:
        LOG_SYS.write(TAG, f"Getting specific product by id: {product_id}.")
        products = await get_product(product_id)
        return products
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/getByCategory/{category}", response_model=List[Product], status_code=200, description="Get a specific products list by category.")
async def getByCategory(category: str):
    try:
        LOG_SYS.write(TAG, f"Getting products by search category: {category}.")
        products = await get_product_by_category(category)
        return products
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getBySearch/{search_string}", response_model=List[Product], status_code=200, description="Get a specific products list by searching string.")
async def getBySearch(search_string: str):
    try:
        LOG_SYS.write(TAG, f"Getting products by search string: {search_string}.")
        products = await get_product_by_search(search_string)
        return products
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sortingBy/{criteria}", response_model=List[Product], status_code=200, description="Get a specific products list sorted by a specific criteria.")
async def sortingBy(criteria: str, asc: bool):
    try:
        LOG_SYS.write(TAG, f"Sort products by a specific criteria: {criteria} and by asc: {asc}.")
        products = await sort_product(criteria, asc)
        return products
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/getFilter", response_model=List[Product], status_code=200, description="Get a specific products list by combo filter.")
async def getFilter(category: str = None, search_string: str = None, criteria: str = None):
    try:
        LOG_SYS.write(TAG, f"Getting products by combo filter.")
        products = await filter_product(category, search_string, criteria)
        return products
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/insertProduct", status_code=201, description="Insert a new product in the database.")
async def insertProduct(product: Product):
    try:
        LOG_SYS.write(TAG, f"Insert new product information with id: {product._id}.")
        result = await insert_product(product)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/deleteProduct/{product_id}", status_code=200, description="Delete a specific product information by id.")
async def deleteProduct(product_id: str):
    try:
        LOG_SYS.write(TAG, f"Delete existing product information with id: {product_id}.")
        result = await delete_product(product_id)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/updateProduct", status_code=200, description="Update a specific product information by id.")
async def updateProduct(product_id: str, product: Product):
    try:
        LOG_SYS.write(TAG, f"Update existing product information with id: {product_id}.")
        result = await update_product(product)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/', status_code=200, tags=["root"])
@app.get('/about', status_code=200, tags=["root"])
async def about():
    return {"App Name": "WTFunko"}

###################################################################################################

def welcome_message():
    LOG_SYS.write(TAG, "__          _________ ______           _          ")   
    LOG_SYS.write(TAG, "\ \        / /__   __|  ____|         | |         ")
    LOG_SYS.write(TAG, " \ \  /\  / /   | |  | |__ _   _ _ __ | | _____   ")
    LOG_SYS.write(TAG, "  \ \/  \/ /    | |  |  __| | | | '_ \| |/ / _ \  ")
    LOG_SYS.write(TAG, "   \  /\  /     | |  | |  | |_| | | | |   < (_) | ")
    LOG_SYS.write(TAG, "    \/  \/      |_|  |_|   \__,_|_| |_|_|\_\___/  ")

def shutdwon():
    try:
        LOG_SYS.write(TAG, "Closing Database MongDB connection.")
        close_connection()
        LOG_SYS.write(TAG, "Shutdown FastAPI server.")
        os.kill(os.getpid(), 9)
    except Exception as e:  
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
    
    
if __name__ == '__main__':
    welcome_message()
    asyncio.run(connect(host="localhost", port=27017, db_name="WTFunko"))
    uvicorn.run(app, host="127.0.0.1", port=8000)
