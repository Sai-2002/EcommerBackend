from fastapi import FastAPI

from src.api.routes.payment_routes import router as payment_router

app = FastAPI(title="Payment Service")

app.include_router(payment_router, prefix="/payments")


@app.get("/")
def home():
    return {"service": "payment-service", "status": "running"}
