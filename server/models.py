# Utils
from typing import List, Dict, Tuple, Any
from pydantic import BaseModel

DB_NAME = "WTFunko"

class User(BaseModel):
    uid: int
    username: str
    email: str
    password: str

class OrderUser(BaseModel):
    uid: int
    username: str
    email: str
    
class Product(BaseModel):
    uid: int
    title: str
    product_type: str
    price: float
    interest: List[str]
    license: List[str]
    tags: List[str]
    vendor: str
    form_factor: List[str]
    feature: List[str]
    related: List[int]
    description: str
    img: str

class Order(BaseModel):
    uid: int
    user: OrderUser
    products: List[Tuple[Product, int]]
    total: float
    date: str
    status: str
