import uuid
from enum import Enum


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Payment:
    def __init__(
        self,
        order_id: uuid.UUID,
        user_id: uuid.UUID,
        amount: float,
        payment_method: str,
        status: PaymentStatus = PaymentStatus.PENDING,
        id: uuid.UUID = None,
    ):
        self.id = id if id is not None else uuid.uuid4()
        self.order_id = order_id
        self.user_id = user_id
        self.amount = amount
        self.status = status
        self.payment_method = payment_method

        self.validate()

    def validate(self):
        if self.amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if not self.payment_method or not self.payment_method.strip():
            raise ValueError("Payment method cannot be empty")
