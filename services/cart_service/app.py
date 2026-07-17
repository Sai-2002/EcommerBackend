from fastapi import FastAPI

from src.api.routes.cart_routes import router as cart_router

app = FastAPI(title="Cart Service")

app.include_router(cart_router, prefix="/cart")


@app.get("/")
def home():
    return {"service": "cart-service", "status": "running"}
