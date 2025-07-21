from pydantic import BaseModel, Field
from typing import List, Optional


class ProductSize(BaseModel):
    size: str
    quantity: int


class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[ProductSize]


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float


class OrderItem(BaseModel):
    productId: str
    qty: int


class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]


class OrderItemResponse(BaseModel):
    qty: int
    productDetails: ProductResponse


class OrderResponse(BaseModel):
    id: str
    items: List[OrderItemResponse]
    total: float
