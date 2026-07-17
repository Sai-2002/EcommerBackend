from fastapi import FastAPI
from src.api.routes.product_routes import router as product_router

app = FastAPI(title="Product Service")

app.include_router(product_router, prefix="/products")


@app.get("/")
def home():
    return {"service": "product-service", "status": "running"}
