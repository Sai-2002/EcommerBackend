from ...domain.entities.product import Product
from ...domain.interfaces.product_repository import ProductRepositoryInterface


class CreateProductUseCase:
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    def execute(
        self,
        name: str,
        description: str,
        price: float,
        stock_quantity: int,
        category_id=None,
    ) -> dict:
        if price < 0:
            raise ValueError("Product price cannot be negative")
        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")

        # Create domain entity (triggers validation)
        product = Product(
            name=name,
            description=description,
            price=price,
            stock_quantity=stock_quantity,
            category_id=category_id,
        )

        # Save via repository
        saved_product = self.product_repository.save(product)

        return {
            "id": str(saved_product.id),
            "name": saved_product.name,
            "description": saved_product.description,
            "price": saved_product.price,
            "stock_quantity": saved_product.stock_quantity,
            "category_id": str(saved_product.category_id) if saved_product.category_id else None,
            "is_active": saved_product.is_active,
        }
