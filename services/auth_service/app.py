from fastapi import FastAPI
from src.api.routes.auth_routes import router as auth_router

app = FastAPI(title="Auth Service")

app.include_router(auth_router, prefix="/auth")


@app.get("/")
def home():
    return {"service": "auth-service", "status": "running"}