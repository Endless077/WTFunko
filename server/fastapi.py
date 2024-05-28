# Fastapi
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
              description="A simple and fast api suite for a test suite for machine learning models.",
              summary="Some easy API for a ML Test Suite.",
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


###################################################################################################
# Users

# Get User
@app.get("/getUser", status_code=200, response_model=User, description="")
async def getUser(username: str, email: str):
    try:
        user_data = get_user(username, email)
        return user_data
    except HTTPException as e:
        raise e

# Insert User
@app.post("/insertUser", status_code=201, description="")
async def insertUser(user: User):
    try:
        result = insert_user(user)
        return {"message": result}
    except HTTPException as e:
        raise e

# Delete User
@app.delete("/user/{username}", status_code=200, description="")
async def delete_existing_user(username: str):
    try:
        result = delete_user(username)
        return {"message": result}
    except HTTPException as e:
        raise e

# Update User
@app.put("/updateUser", status_code=200, description="")
async def updateUser(user: User):
    try:
        result = update_user(user)
        return {"message": result}
    except HTTPException as e:
        raise e
      
###################################################################################################
# Orders

# Get User Orders
@app.get("/getUserOrders", status_code=200, response_model=List[Order], description="")
async def getUserOrders(username: str):
    try:
        orders = get_orders(username)
        return orders
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Order Infos
@app.get("/getOrderInfo", status_code=200, response_model=Order, description="")
async def getOrderInfo(order_id: str):
    try:
        order_info = get_order_info(order_id)
        return order_info
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Insert Order
@app.post("/insertOrder", status_code=201, description="")
async def insertOrder(order: Order):
    try:
        result = insert_order(order)
        return {"message": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete Order
@app.delete("/deleteOrder/{order_id}", status_code=200, description="")
async def deleteOrder(order_id: str):
    try:
        result = delete_order(order_id)
        return {"message": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update Order
app.put("/updateOrder", status_code=200, description="")
async def updateOrder(order: Order):
    try:
        result = update_order(order)
        return {"message": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
###################################################################################################
# Products

# Get all Funko
@app.get("/getAllFunkos", response_model=List[Product], status_code=200, description="")
async def getAllFunkos():
    try:
        funko_list = get_all_funkos()
        return funko_list
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Funko info by ID
@app.get("/getFunkoInfo/{funk_id}", response_model=Product, status_code=200, description="")
async def getFunkInfo(funk_id: str):
    try:
        funko_info = get_funko_info(funk_id)
        return funko_info
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Funko by category
@app.get("/getByCategory/{category}", response_model=List[Product], status_code=200, description="")
async def getByCategory(category: str):
    try:
        funko_list = get_funko_by_category(category)
        return funko_list
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Search Funko
@app.get("/getResearch/{search_string}", response_model=List[Product], status_code=200, description="")
async def get_funko_by_search(search_string: str):
    try:
        funko_list = get_funko_by_search(search_string)
        return funko_list
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sort Funko by criteria
@app.get("/sortingby/{criteria}", response_model=List[Product], status_code=200, description="")
async def sort_funko(criteria: str, asc: bool):
    try:
        sorted_funko = sort_funko(criteria, asc)
        return sorted_funko
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Insert new Funko
@app.post("/insertFunko", status_code=201, description="")
async def insert_new_funko(funko: Product):
    try:
        result = insert_funko(funko)
        return {"message": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete Funko by ID
@app.delete("/deleteFunko/{funk_id}", status_code=200, description="")
async def deleteFunko(funk_id: str):
    try:
        result = delete_funko(funk_id)
        return {"message": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update Funko
@app.put("/updateFunko", status_code=200, description="")
async def updateFunko(funko: Product):
    try:
        result = update_funko(funko)
        return {"message": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

###################################################################################################
# Utils

@app.get("/", status_code=200, tags=["root"])
@app.get("/about", status_code=200,tags=["About"])
async def about():
    return {"message": "Hello, world!"}

###################################################################################################

if __name__ == '__main__':
    print(" ________               _        _       _______  _____  ")
    print("|_   __  |             / |_     / \     |_   __ \|_   _| ")
    print("  | |_ \_|,--.   .--. `| |-'   / _ \      | |__) | | |   ")
    print("  |  _|  `'_\ : ( (`\] | |    / ___ \     |  ___/  | |   ")
    print(" _| |_   // | |, `'.'. | |, _/ /   \ \_  _| |_    _| |_  ")
    print("|_____|  \'-;__/[\__) )\__/|____| |____||_____|  |_____| ")
    
    LOG_SYS = Logger(f"logs_{dt.now}.txt","../source/logs")
    uvicorn.run(app, host='127.0.0.1', port=8080)

###################################################################################################
