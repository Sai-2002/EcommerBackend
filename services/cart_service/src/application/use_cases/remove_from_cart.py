import uuid

from ...domain.interfaces.cart_repository import CartRepositoryInterface


class RemoveFromCartUseCase:
    def __init__(self, repository: CartRepositoryInterface):
        self.repository = repository

    def execute(self, item_id: str) -> None:
        self.repository.delete(uuid.UUID(item_id))
