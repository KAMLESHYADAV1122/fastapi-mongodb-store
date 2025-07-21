from fastapi import APIRouter, status
from bson import ObjectId
from database import orders_collection, products_collection
from models import OrderCreate, OrderResponse
from utils import get_pagination
from typing import List

router = APIRouter()


@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    order_doc = {
        "userId": order.userId,
        "items": [{"productId": item.productId, "qty": item.qty} for item in order.items]
    }
    result = await orders_collection.insert_one(order_doc)
    return {"id": str(result.inserted_id)}


@router.get("/orders/{user_id}")
async def get_orders(user_id: str, limit: int = 10, offset: int = 0):
    query = {"userId": user_id}
    total = await orders_collection.count_documents(query)

    cursor = orders_collection.find(query).skip(offset).limit(limit)

    data = []
    async for order in cursor:
        items = []
        total_price = 0.0

        for item in order["items"]:
            product = await products_collection.find_one({"_id": ObjectId(item["productId"])})
            if product:
                items.append({
                    "qty": item["qty"],
                    "productDetails": {
                        "name": product["name"],
                        "price": product["price"],
                        "id": str(product["_id"])
                    }
                })
                total_price += item["qty"] * product["price"]

        data.append({
            "id": str(order["_id"]),
            "items": items,
            "total": total_price
        })

    return {
        "data": data,
        "page": get_pagination(offset, limit, total)
    }
