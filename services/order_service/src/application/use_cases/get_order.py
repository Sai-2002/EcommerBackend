import uuid
from ...infrastructure.repository.order_repository import OrderRepository


class GetOrderUseCase:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def execute(self, order_id: uuid.UUID) -> dict:
        order = self.repo.find_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        return {
            "order_id": str(order.id),
            "user_id": str(order.user_id),
            "status": order.status,
            "total_amount": order.total_amount,
            "created_at": str(order.created_at) if order.created_at else None,
        }
