import uuid
from ...domain.interfaces.product_repository import ProductRepositoryInterface


class DeleteProductUseCase:
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    def execute(self, product_id: uuid.UUID) -> None:
        self.product_repository.delete(product_id)
