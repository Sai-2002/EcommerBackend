import uuid

from ...domain.interfaces.payment_repository import PaymentRepositoryInterface


class GetPaymentByOrderUseCase:
    def __init__(self, payment_repository: PaymentRepositoryInterface):
        self.payment_repository = payment_repository

    def execute(self, order_id: uuid.UUID) -> dict:
        payment = self.payment_repository.find_by_order_id(order_id)
        if not payment:
            raise ValueError("No payment found for this order")

        return {
            "payment_id": str(payment.id),
            "order_id": str(payment.order_id),
            "user_id": str(payment.user_id),
            "amount": payment.amount,
            "status": payment.status,
            "payment_method": payment.payment_method,
        }
