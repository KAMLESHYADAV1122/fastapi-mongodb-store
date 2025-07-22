from fastapi import APIRouter, status
from database import db
from schemas import OrderCreate
from bson import ObjectId

router = APIRouter()

@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    res = await db.orders.insert_one(order.dict())
    return {"id": str(res.inserted_id)}

@router.get("/orders/{user_id}")
async def get_orders(user_id: str, limit: int = 10, offset: int = 0):
    query = {"userId": user_id}
    cursor = db.orders.find(query).skip(offset).limit(limit)

    orders_list = []
    async for order in cursor:
        items_with_details = []
        for item in order["items"]:
            product = await db.products.find_one({"_id": ObjectId(item["productId"])})
            if product:
                items_with_details.append({
                    "productDetails": {
                        "id": str(product["_id"]),
                        "name": product["name"],
                        "price": product["price"]
                    },
                    "qty": item["qty"]
                })

        total = sum(i["productDetails"]["price"] * i["qty"] for i in items_with_details)
        orders_list.append({
            "id": str(order["_id"]),
            "items": items_with_details,
            "total": total
        })

    return {
        "data": orders_list,
        "page": {
            "next": offset + limit,
            "limit": len(orders_list),
            "previous": max(offset - limit, 0)
        }
    }
