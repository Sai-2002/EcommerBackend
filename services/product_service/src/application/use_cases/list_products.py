import uuid
from typing import Optional
from ...domain.interfaces.product_repository import ProductRepositoryInterface


class ListProductsUseCase:
    def __init__(self, product_repository: ProductRepositoryInterface):
        self.product_repository = product_repository

    def execute(self, category_id: Optional[uuid.UUID] = None) -> list:
        if category_id:
            products = self.product_repository.find_by_category(category_id)
        else:
            products = self.product_repository.find_all()

        return [
            {
                "id": str(p.id),
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "stock_quantity": p.stock_quantity,
                "category_id": str(p.category_id) if p.category_id else None,
                "is_active": p.is_active,
            }
            for p in products
        ]
