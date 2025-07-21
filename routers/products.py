from fastapi import APIRouter, Query, status
from bson import ObjectId
from database import products_collection
from models import ProductCreate, ProductResponse
from typing import List, Optional
from utils import get_pagination

router = APIRouter()


@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    result = await products_collection.insert_one(product.dict())
    return {"id": str(result.inserted_id)}


@router.get("/products")
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes.size"] = size

    total = await products_collection.count_documents(query)
    cursor = products_collection.find(query).skip(offset).limit(limit)

    products = []
    async for doc in cursor:
        products.append({
            "id": str(doc["_id"]),
            "name": doc["name"],
            "price": doc["price"]
        })

    return {
        "data": products,
        "page": get_pagination(offset, limit, total)
    }
    