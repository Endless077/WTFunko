# Fastapi
from fastapi import FastAPI, HTTPException, Request, Response

# Security & Middleware
from fastapi.security import *
from fastapi.middleware.cors import CORSMiddleware

# Unvicorn
import uvicorn

# Utils
from server.services import *

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

@app.get("/", status_code=200)
@app.get("/about", status_code=200)
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
    
    uvicorn.run(app, host='127.0.0.1', port=8080)

###################################################################################################
