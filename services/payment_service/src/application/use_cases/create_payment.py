from uuid import UUID

from ...domain.entities.payment import Payment
from ...domain.interfaces.payment_repository import PaymentRepositoryInterface


class CreatePaymentUseCase:
    def __init__(self, payment_repository: PaymentRepositoryInterface):
        self.payment_repository = payment_repository

    def execute(self, order_id: str, user_id: str, amount: float, payment_method: str) -> dict:
        # Check for duplicate payment for this order
        existing = self.payment_repository.find_by_order_id(UUID(order_id))
        if existing:
            raise ValueError("Payment already exists for this order")

        # Create domain entity (triggers validation)
        payment = Payment(
            order_id=UUID(order_id),
            user_id=UUID(user_id),
            amount=amount,
            payment_method=payment_method,
        )

        # Persist
        saved = self.payment_repository.save(payment)

        return {
            "payment_id": str(saved.id),
            "order_id": str(saved.order_id),
            "amount": saved.amount,
            "status": saved.status,
            "payment_method": saved.payment_method,
        }
