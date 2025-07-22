from typing import List, Optional
from pydantic import BaseModel, Field


class SizeModel(BaseModel):
    size: str
    quantity: int


class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[SizeModel]


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float


class ProductListResponse(BaseModel):
    data: List[ProductResponse]
    page: dict


class OrderItem(BaseModel):
    productId: str
    qty: int


class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]


class OrderItemResponse(BaseModel):
    productDetails: ProductResponse
    qty: int


class OrderResponse(BaseModel):
    id: str


class OrderListResponse(BaseModel):
    data: List[dict]
    page: dict
