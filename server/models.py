"""
Defines various classes for handling the database objects.
"""

from typing import List, Tuple
from pydantic import BaseModel, Field
from bson.objectid import ObjectId



DB_NAME = "WTFunko"

class User(BaseModel):
    id: int = Field(alias='_id')
    username: str
    email: str
    password: str


class OrderUser(BaseModel):
    id: int = Field(alias='_id')
    username: str
    email: str
    

class Product(BaseModel):
    id: int = Field(alias='_id')
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
    id: int = Field(alias='_id')
    user: OrderUser
    products: List[Tuple[Product, int]]
    total: float
    date: str
    status: str
