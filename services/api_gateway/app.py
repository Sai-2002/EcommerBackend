from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from src.routes.gateway_router import router

load_dotenv(Path(__file__).resolve().parent / ".env")

app = FastAPI(title="API Gateway")
app.include_router(router)


@app.get("/")
def health():
    return {"service": "api-gateway", "status": "running"}
