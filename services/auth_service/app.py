from fastapi import FastAPI

app = FastAPI(title = "Auth Service")

@app.get("/")
def home():
    return {
        "message" : "Auth Service is executing Properly"
    }