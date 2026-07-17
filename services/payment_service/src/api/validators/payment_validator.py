from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreatePaymentRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "order_id": "123e4567-e89b-12d3-a456-426614174000",
            "user_id": "123e4567-e89b-12d3-a456-426614174001",
            "amount": 99.99,
            "payment_method": "card"
        }
    })

    order_id: UUID
    user_id: UUID
    amount: float
    payment_method: str
