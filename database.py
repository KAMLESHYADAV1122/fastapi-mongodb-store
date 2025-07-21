from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

MONGO_URL = "mongodb://localhost:27017"  # or use MongoDB Atlas URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["ecommerce_db"]

products_collection = db["products"]
orders_collection = db["orders"]

