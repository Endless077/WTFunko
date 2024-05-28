# Services
import pymongo
from bson import ObjectId
from pymongo import MongoClient

# Models
from server.models import *

###################################################################################################

async def get_user(username: str, password: str) -> User:
    pass

async def insert_user(user_data: User) -> str:
    pass

async def delete_user(username: str) -> str:
    pass

async def update_user(user_data: User) -> str:
    pass

###################################################################################################

async def get_orders(username: str) -> List[Order]:
    pass

async def get_order_info(order_id: str) -> Order:
    pass

async def insert_order(order_data: Order) -> str:
    pass

async def delete_order(order_id: str) -> str:
    pass

async def update_order(order_data: User) -> str:
    pass

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