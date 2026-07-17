import uuid
from ...domain.entities.order import Order
from ...infrastructure.repository.order_repository import OrderRepository


class CreateOrderUseCase:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def execute(self, user_id: str, items: list[dict]) -> dict:
        total_amount = sum(item["quantity"] * item["unit_price"] for item in items)
        order = Order(user_id=uuid.UUID(user_id), total_amount=total_amount)
        saved_order = self.repo.save(order)
        self.repo.save_items(saved_order.id, items)
        return {
            "order_id": str(saved_order.id),
            "user_id": str(saved_order.user_id),
            "status": saved_order.status,
            "total_amount": saved_order.total_amount,
        }
