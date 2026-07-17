from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class CreateProductRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Sample Product",
            "description": "A sample product description",
            "price": 29.99,
            "stock_quantity": 100,
            "category_id": None
        }
    })

    name: str
    description: str = ""
    price: float
    stock_quantity: int
    category_id: Optional[UUID] = None


class UpdateProductRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Updated Product",
            "description": "Updated description",
            "price": 39.99,
            "stock_quantity": 50
        }
    })

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None


class CreateCategoryRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Electronics",
            "description": "Electronic products"
        }
    })

    name: str
    description: str = ""
