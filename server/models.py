from typing import List, Dict, Tuple, Any
from pydantic import BaseModel

class User(BaseModel):
    ID: str
    Username: str
    Email: str
    Password: str
    
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
    order_id: str
    user: Dict[str, Any]
    products: List[Tuple[Product, int]]
    total: float
    date: str
    status: str
