import uuid

from ...domain.entities.cart_item import CartItem
from ...domain.interfaces.cart_repository import CartRepositoryInterface


class AddToCartUseCase:
    def __init__(self, repository: CartRepositoryInterface):
        self.repository = repository

    def execute(self, user_id: str, product_id: str, quantity: int = 1) -> dict:
        user_id_uuid = uuid.UUID(user_id)
        product_id_uuid = uuid.UUID(product_id)

        existing = self.repository.find_by_user_and_product(user_id_uuid, product_id_uuid)

        if existing:
            new_qty = existing.quantity + quantity
            updated = self.repository.update_quantity(existing.id, new_qty)
            return {
                "id": str(updated.id),
                "user_id": str(updated.user_id),
                "product_id": str(updated.product_id),
                "quantity": updated.quantity,
            }
        else:
            item = CartItem(user_id=user_id_uuid, product_id=product_id_uuid, quantity=quantity)
            saved = self.repository.save(item)
            return {
                "id": str(saved.id),
                "user_id": str(saved.user_id),
                "product_id": str(saved.product_id),
                "quantity": saved.quantity,
            }
