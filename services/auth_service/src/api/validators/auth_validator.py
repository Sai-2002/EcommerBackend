from pydantic import BaseModel, EmailStr, ConfigDict


class RegisterRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "user@example.com",
            "password": "securepassword123"
        }
    })

    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "email": "user@example.com",
            "password": "securepassword123"
        }
    })

    email: EmailStr
    password: str
