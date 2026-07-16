from fastapi import FastAPI

app = FastAPI(title = "Ecommerce Backend")

@app.get("/")
def home():
    return {
        "message": "Welcome Home"
    }