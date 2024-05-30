# FastAPI
from fastapi import FastAPI, HTTPException, Request, Response

# Security & Middleware
from fastapi.security import *
from fastapi.middleware.cors import CORSMiddleware

# Unvicorn
import uvicorn

# Date time
from datetime import datetime as dt

# Utils
from utils import Logger
from server.models import *
from server.services import *

# Setup Logging System
LOG_SYS = None

###################################################################################################

# To Run: uvicorn server:app --host 127.0.0.1 --port 8080 --reload
# To Run: uvicorn server:app --host 127.0.0.1 --port 8080

TAG = "FastAPI"

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

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TAG = "FastAPI"

###################################################################################################
# Users

# Get User
@app.get("/getUser", status_code=200, response_model=User, description="Get a specific user by username or email.")
async def getUser(username: str, email: str):
    try:
        LOG_SYS.write(TAG, f"Getting user information with username: {username} or email: {email}.")
        user_data = get_user(username, email)
        return {"data": user_data}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An error occured with Excepytion: {e}")
        raise e

# Insert User
@app.post("/insertUser", status_code=201, description="Insert a new user information into database.")
async def insertUser(user: User):
    try:
        LOG_SYS.write(TAG, f"Insert new user information into db with username: {user.Username}.")
        result = insert_user(user)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Delete User
@app.delete("/user/{username}", status_code=200, description="Delete a specific user information by username.")
async def delete_existing_user(username: str):
    try:
        LOG_SYS.write(TAG, f"Delete existing user information with username: {username}.")
        result = delete_user(username)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Update User
@app.put("/updateUser", status_code=200, description="Update a specific user information by username.")
async def updateUser(username: str, user: User):
    try:
        LOG_SYS.write(TAG, f"Update existing user information with username: {username}.")
        result = update_user(user)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))
      
###################################################################################################
# Orders

# Get User Orders
@app.get("/getUserOrders", status_code=200, response_model=List[Order], description="Get all orders form a user account by username.")
async def getUserOrders(username: str):
    try:
        LOG_SYS.write(TAG, f"Getting all orders information from user account with username: {username}.")
        orders = get_orders(username)
        return {"data": orders}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Get Order Infos
@app.get("/getOrderInfo", status_code=200, response_model=Order, description="Get a specific order infos by id.")
async def getOrderInfo(order_id: str):
    try:
        LOG_SYS.write(TAG, f"Getting all information of a specifc order with id: {order_id}.")
        order_info = get_order_info(order_id)
        return {"data": order_info}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Insert Order
@app.post("/insertOrder", status_code=201, description="Insert a new order information into database")
async def insertOrder(order: Order):
    try:
        LOG_SYS.write(TAG, f"Insert new order information with username: {order.order_id}.")
        result = insert_order(order)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Delete Order
@app.delete("/deleteOrder/{order_id}", status_code=200, description="Delete a specific order information by id.")
async def deleteOrder(order_id: str):
    try:
        LOG_SYS.write(TAG, f"Delete existing order information with id: {order_id}.")
        result = delete_order(order_id)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Update Order
app.put("/updateOrder", status_code=200, description="Update a specific order information by id.")
async def updateOrder(order_id: str, order: Order):
    try:
        LOG_SYS.write(TAG, f"Update existing order information with id: {order_id}.")
        result = update_order(order)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))
      
###################################################################################################
# Products

# Get all Funko
@app.get("/getAllFunkos", response_model=List[Product], status_code=200, description="")
async def getAllFunkos():
    try:
        LOG_SYS.write(TAG, f"Getting all product from Database.")
        funkos = get_all_funkos()
        return {"data": funkos}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Get Funko info by ID
@app.get("/getFunkoInfo/{funk_id}", response_model=Product, status_code=200, description="")
async def getFunkInfo(funk_id: str):
    try:
        LOG_SYS.write(TAG, f"Getting specific product infos by id: {funk_id}.")
        funko_info = get_funko_info(funk_id)
        return {"data": funko_info}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Get Funko by category
@app.get("/getByCategory/{category}", response_model=List[Product], status_code=200, description="")
async def getByCategory(category: str):
    try:
        LOG_SYS.write(TAG, f"Getting products by search category: {category}.")
        funkos = get_funko_by_category(category)
        return {"data": funkos}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Search Funko
@app.get("/getResearch/{search_string}", response_model=List[Product], status_code=200, description="")
async def get_funko_by_search(search_string: str):
    try:
        LOG_SYS.write(TAG, f"Getting products by search string: {search_string}.")
        funkos = get_funko_by_search(search_string)
        return {"data": funkos}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Sort Funko by criteria
@app.get("/sortingby/{criteria}", response_model=List[Product], status_code=200, description="")
async def sort_funko(criteria: str, asc: bool):
    try:
        LOG_SYS.write(TAG, f"Sort products by a specific criteria: {criteria} and by asc: {asc}.")
        funkos = sort_funko(criteria, asc)
        return {"data": funkos}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Insert new Funko
@app.post("/insertFunko", status_code=201, description="")
async def insert_new_funko(funko: Product):
    try:
        LOG_SYS.write(TAG, f"Insert new product information with id: {funko.uid}.")
        result = insert_funko(funko)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Delete Funko by ID
@app.delete("/deleteFunko/{funk_id}", status_code=200, description="")
async def deleteFunko(funk_id: str):
    try:
        LOG_SYS.write(TAG, f"Delete existing product information with id: {funk_id}.")
        result = delete_funko(funk_id)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Update Funko
@app.put("/updateFunko", status_code=200, description="")
async def updateFunko(funk_id: str, funko: Product):
    try:
        LOG_SYS.write(TAG, f"Update existing product information with id: {funk_id}.")
        result = update_funko(funko)
        return {"message": result}
    except HTTPException as e:
        LOG_SYS.write(TAG, f"An HTTP error occured with Exception: {e}")
        raise e
    except Exception as e:
        LOG_SYS.write(TAG, f"An error occured with Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

###################################################################################################
# Utils

@app.get("/", status_code=200, tags=["root"])
@app.get("/about", status_code=200,tags=["About"])
async def about():
    return {"message": "Hello, world!"}

###################################################################################################

if __name__ == '__main__':
    LOG_SYS = Logger(f"logs_{dt.now}.txt","../source/logs")
    LOG_SYS(TAG, "__          _________ ______           _          ")   
    LOG_SYS(TAG, "\ \        / /__   __|  ____|         | |         ")
    LOG_SYS(TAG, " \ \  /\  / /   | |  | |__ _   _ _ __ | | _____   ")
    LOG_SYS(TAG, "  \ \/  \/ /    | |  |  __| | | | '_ \| |/ / _ \  ")
    LOG_SYS(TAG, "   \  /\  /     | |  | |  | |_| | | | |   < (_) | ")
    LOG_SYS(TAG, "    \/  \/      |_|  |_|   \__,_|_| |_|_|\_\___/  ")
    
    db_name = "WTFunko"
    collections = ["Users", "Products", "Orders"]
    
    init_database(db_name, collections)
    
    # Uncomment only the first time
    #fill_collection(db_name, "Products", "../source/json/funko.json")
    
    uvicorn.run(app, host='127.0.0.1', port=8080)

###################################################################################################
