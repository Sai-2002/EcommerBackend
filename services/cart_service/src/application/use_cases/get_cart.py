import uuid

from ...domain.interfaces.cart_repository import CartRepositoryInterface


class GetCartUseCase:
    def __init__(self, repository: CartRepositoryInterface):
        self.repository = repository

    def execute(self, user_id: str) -> list[dict]:
        items = self.repository.find_by_user_id(uuid.UUID(user_id))
        return [
            {
                "id": str(item.id),
                "user_id": str(item.user_id),
                "product_id": str(item.product_id),
                "quantity": item.quantity,
            }
            for item in items
        ]
