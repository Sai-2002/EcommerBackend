import uuid

from ...domain.interfaces.cart_repository import CartRepositoryInterface


class ClearCartUseCase:
    def __init__(self, repository: CartRepositoryInterface):
        self.repository = repository

    def execute(self, user_id: str) -> None:
        self.repository.clear(uuid.UUID(user_id))
