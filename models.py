from bson import ObjectId

def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"]
    }

def order_helper(order, product_map) -> dict:
    total = 0
    items = []
    for item in order["items"]:
        product = product_map.get(item["productId"])
        if product:
            total += product["price"] * item["qty"]
            items.append({
                "productDetails": {
                    "id": str(product["_id"]),
                    "name": product["name"]
                },
                "qty": item["qty"]
            })
    return {
        "id": str(order["_id"]),
        "items": items,
        "total": total
    }
