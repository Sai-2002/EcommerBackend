from fastapi import FastAPI
from src.api.routes.order_routes import router as order_router

app = FastAPI(title="Order Service")

app.include_router(order_router, prefix="/orders")


@app.get("/")
def home():
    return {"service": "order-service", "status": "running"}
