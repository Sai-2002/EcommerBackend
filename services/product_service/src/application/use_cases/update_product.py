import uuid
from ...domain.entities.product import Product
from ...domain.interfaces.product_repository import ProductRepositoryInterface


class UpdateProductUseCase:
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    def execute(self, product_id: uuid.UUID, **kwargs) -> dict:
        existing = self.product_repository.find_by_id(product_id)
        if not existing:
            raise ValueError("Product not found")

        # Apply updates, falling back to existing values
        updated_product = Product(
            id=existing.id,
            name=kwargs.get("name", existing.name),
            description=kwargs.get("description", existing.description),
            price=kwargs.get("price", existing.price),
            stock_quantity=kwargs.get("stock_quantity", existing.stock_quantity),
            category_id=kwargs.get("category_id", existing.category_id),
            is_active=kwargs.get("is_active", existing.is_active),
        )

        saved_product = self.product_repository.update(updated_product)

        return {
            "id": str(saved_product.id),
            "name": saved_product.name,
            "description": saved_product.description,
            "price": saved_product.price,
            "stock_quantity": saved_product.stock_quantity,
            "category_id": str(saved_product.category_id) if saved_product.category_id else None,
            "is_active": saved_product.is_active,
        }
