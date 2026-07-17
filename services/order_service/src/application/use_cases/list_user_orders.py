import uuid
from ...infrastructure.repository.order_repository import OrderRepository


class ListUserOrdersUseCase:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def execute(self, user_id: uuid.UUID) -> list[dict]:
        orders = self.repo.find_by_user_id(user_id)
        return [
            {
                "order_id": str(order.id),
                "user_id": str(order.user_id),
                "status": order.status,
                "total_amount": order.total_amount,
                "created_at": str(order.created_at) if order.created_at else None,
            }
            for order in orders
        ]
