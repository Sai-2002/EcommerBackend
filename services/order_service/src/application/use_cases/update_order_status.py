import uuid
from ...infrastructure.repository.order_repository import OrderRepository


class UpdateOrderStatusUseCase:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def execute(self, order_id: uuid.UUID, status: str) -> dict:
        valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
        if status not in valid_statuses:
            raise ValueError("Invalid status")
        order = self.repo.find_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        updated = self.repo.update_status(order_id, status)
        return {
            "order_id": str(updated.id),
            "user_id": str(updated.user_id),
            "status": updated.status,
            "total_amount": updated.total_amount,
            "created_at": str(updated.created_at) if updated.created_at else None,
        }
