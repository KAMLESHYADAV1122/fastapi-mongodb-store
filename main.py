from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import products, orders

app = FastAPI()

# 🟡 CORS Middleware lagana zaroori hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sabhi origins allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers include karo
app.include_router(products.router)
app.include_router(orders.router)
