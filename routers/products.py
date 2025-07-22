from fastapi import APIRouter, status, Query
from database import db
from schemas import ProductCreate, ProductResponse, ProductListResponse
from bson import ObjectId
from typing import List, Optional
import re

router = APIRouter()

@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    res = await db.products.insert_one(product.dict())
    return {"id": str(res.inserted_id)}

@router.get("/products", response_model=ProductListResponse)
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    query = {}
    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}
    if size:
        query["sizes"] = {"$elemMatch": {"size": size}}

    cursor = db.products.find(query).skip(offset).limit(limit)
    products = []
    async for product in cursor:
        products.append(ProductResponse(
            id=str(product["_id"]),
            name=product["name"],
            price=product["price"]
        ))

    return {
        "data": products,
        "page": {
            "next": offset + limit,
            "limit": len(products),
            "previous": max(offset - limit, 0)
        }
    }
