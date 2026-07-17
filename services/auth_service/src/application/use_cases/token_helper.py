import jwt
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(BASE_DIR / ".env")

def generate_token(user_id: str, email: str) -> dict:

    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }

    token = jwt.encode(
        payload=payload,
        key=os.getenv("JWT_SECRET"),
        algorithm="HS256"
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt=token,
            key=os.getenv("JWT_SECRET"),
            algorithms=["HS256"]
        )
        return payload

    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")

    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
