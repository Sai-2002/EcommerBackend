from typing import Optional
from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session

from ...infrastructure.session import get_db
from ...infrastructure.repository.product_repository import ProductRepository
from ...infrastructure.repository.category_repository import CategoryRepository
from ...application.use_cases.create_product import CreateProductUseCase
from ...application.use_cases.get_product import GetProductUseCase
from ...application.use_cases.list_products import ListProductsUseCase
from ...application.use_cases.update_product import UpdateProductUseCase
from ...application.use_cases.delete_product import DeleteProductUseCase
from ...application.use_cases.create_category import CreateCategoryUseCase
from ...application.use_cases.list_categories import ListCategoriesUseCase
from ..validators.product_validator import (
    CreateProductRequest,
    UpdateProductRequest,
    CreateCategoryRequest,
)


class ProductController:

    def create_product(self, request: CreateProductRequest, db: Session = Depends(get_db)):
        product_repository = ProductRepository(db)
        use_case = CreateProductUseCase(product_repository)

        result = use_case.execute(
            name=request.name,
            description=request.description,
            price=request.price,
            stock_quantity=request.stock_quantity,
            category_id=request.category_id,
        )

        return result

    def get_product(self, product_id: UUID, db: Session = Depends(get_db)):
        product_repository = ProductRepository(db)
        use_case = GetProductUseCase(product_repository)

        result = use_case.execute(product_id=product_id)

        return result

    def list_products(self, category_id: Optional[UUID] = None, db: Session = Depends(get_db)):
        product_repository = ProductRepository(db)
        use_case = ListProductsUseCase(product_repository)

        result = use_case.execute(category_id=category_id)

        return result

    def update_product(self, product_id: UUID, request: UpdateProductRequest, db: Session = Depends(get_db)):
        product_repository = ProductRepository(db)
        use_case = UpdateProductUseCase(product_repository)

        # Only pass fields that were explicitly set
        update_fields = request.model_dump(exclude_none=True)
        result = use_case.execute(product_id=product_id, **update_fields)

        return result

    def delete_product(self, product_id: UUID, db: Session = Depends(get_db)):
        product_repository = ProductRepository(db)
        use_case = DeleteProductUseCase(product_repository)

        use_case.execute(product_id=product_id)

        return {"message": "Product deleted successfully"}

    def create_category(self, request: CreateCategoryRequest, db: Session = Depends(get_db)):
        category_repository = CategoryRepository(db)
        use_case = CreateCategoryUseCase(category_repository)

        result = use_case.execute(
            name=request.name,
            description=request.description,
        )

        return result

    def list_categories(self, db: Session = Depends(get_db)):
        category_repository = CategoryRepository(db)
        use_case = ListCategoriesUseCase(category_repository)

        result = use_case.execute()

        return result
