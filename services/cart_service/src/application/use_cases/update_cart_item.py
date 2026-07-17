import uuid

from ...domain.interfaces.cart_repository import CartRepositoryInterface


class UpdateCartItemUseCase:
    def __init__(self, repository: CartRepositoryInterface):
        self.repository = repository

    def execute(self, item_id: str, quantity: int) -> dict:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        updated = self.repository.update_quantity(uuid.UUID(item_id), quantity)
        return {
            "id": str(updated.id),
            "user_id": str(updated.user_id),
            "product_id": str(updated.product_id),
            "quantity": updated.quantity,
        }
