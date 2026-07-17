import uuid
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order:
    def __init__(self, user_id: uuid.UUID, total_amount: float, status: OrderStatus = OrderStatus.PENDING):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.status = status
        self.total_amount = total_amount
        self.created_at = None

        self.validate()

    def validate(self):
        if self.total_amount < 0:
            raise ValueError("total_amount cannot be negative")
