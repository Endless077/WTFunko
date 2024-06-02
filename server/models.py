"""
Defines various classes for handling the database objects.
"""

from typing import List, Tuple
from pydantic import BaseModel

DB_NAME = "WTFunko"

class User(BaseModel):
    _id: int
    username: str
    email: str
    password: str

class OrderUser(BaseModel):
    _id: int
    username: str
    email: str
    
class Product(BaseModel):
    _id: int
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
    _id: int
    user: OrderUser
    products: List[Tuple[Product, int]]
    total: float
    date: str
    status: str
