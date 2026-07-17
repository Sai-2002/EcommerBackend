from uuid import UUID
from pydantic import BaseModel, ConfigDict


class OrderItemRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "product_id": "123e4567-e89b-12d3-a456-426614174000",
            "quantity": 2,
            "unit_price": 19.99
        }
    })

    product_id: UUID
    quantity: int
    unit_price: float


class CreateOrderRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "user_id": "123e4567-e89b-12d3-a456-426614174001",
            "items": [
                {
                    "product_id": "123e4567-e89b-12d3-a456-426614174000",
                    "quantity": 2,
                    "unit_price": 19.99
                }
            ]
        }
    })

    user_id: UUID
    items: list[OrderItemRequest]


class UpdateOrderStatusRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "status": "confirmed"
        }
    })

    status: str
