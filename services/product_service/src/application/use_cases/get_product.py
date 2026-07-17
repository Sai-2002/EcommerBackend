import uuid
from ...domain.interfaces.product_repository import ProductRepositoryInterface


class GetProductUseCase:
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    def execute(self, product_id: uuid.UUID) -> dict:
        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        return {
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock_quantity": product.stock_quantity,
            "category_id": str(product.category_id) if product.category_id else None,
            "is_active": product.is_active,
        }
