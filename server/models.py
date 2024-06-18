# Models
from typing import List, Tuple, Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: Optional[int] = Field(-1, alias='_id', description="Unique identifier for the user")
    username: str = Field(..., description="Username of the user")
    email: str = Field(..., description="Email address of the user")
    password: str = Field(..., description="Password of the user")


class OrderUser(BaseModel):
    id: Optional[int] = Field(-1, alias='_id', description="Unique identifier for the user in an order")
    username: str = Field(..., description="Username of the user in an order")
    email: str = Field(..., description="Email address of the user in an order")

 
class Product(BaseModel):
    id: Optional[int] = Field(-1, alias='_id', description="Unique identifier for the product")
    title: str = Field(..., description="Title of the product")
    product_type: str = Field(..., description="Type of the product")
    price: float = Field(..., description="Price of the product")
    quantity: int = Field(..., description="The amount of product in the warehouse.")
    interest: List[str] = Field(..., description="List of interests associated with the product")
    license: List[str] = Field(..., description="List of licenses for the product")
    tags: List[str] = Field(..., description="Tags associated with the product")
    vendor: str = Field(..., description="Vendor of the product")
    form_factor: List[str] = Field(..., description="Form factor of the product")
    feature: List[str] = Field(..., description="Features of the product")
    related: List[int] = Field(..., description="List of related product IDs")
    description: str = Field(..., description="Description of the product")
    img: str = Field(..., description="Image URL of the product")


class ProductFilter(BaseModel):
    category: Optional[str] = Field("All", description="Category to Filter.")
    searchTerm: Optional[str] = Field("", description="Search Term to Filter.")
    pageIndex: Optional[int] = Field(0, description="Index of the page to view.")


class Order(BaseModel):
    id: Optional[int] = Field(-1, alias='_id', description="Unique identifier for the order")
    user: OrderUser = Field(..., description="User associated with the order")
    products: List[Tuple[Product, int]] = Field(..., description="List of products and their quantities in the order")
    total: float = Field(..., description="Total price of the order")
    date: str = Field(..., description="Date of the order")
    status: str = Field(..., description="Status of the order")
