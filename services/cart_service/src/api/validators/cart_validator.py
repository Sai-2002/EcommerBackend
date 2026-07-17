import uuid
from pydantic import BaseModel, ConfigDict


class AddToCartRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "product_id": "3fa85f64-5717-4562-b3fc-2c963f66afb7",
            "quantity": 1
        }
    })

    user_id: uuid.UUID
    product_id: uuid.UUID
    quantity: int = 1


class UpdateCartItemRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "quantity": 3
        }
    })

    quantity: int
