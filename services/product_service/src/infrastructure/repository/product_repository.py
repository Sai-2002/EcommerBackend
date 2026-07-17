from typing import Optional
import uuid
from sqlalchemy.orm import Session
from ..model.product import Product as ProductModel
from ...domain.interfaces.product_repository import ProductRepositoryInterface
from ...domain.entities.product import Product as DomainProduct


class ProductRepository(ProductRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def save(self, product: DomainProduct) -> ProductModel:
        db_product = ProductModel()
        db_product.id = product.id
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.stock_quantity = product.stock_quantity
        db_product.category_id = product.category_id
        db_product.is_active = product.is_active
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def find_by_id(self, id: uuid.UUID) -> Optional[ProductModel]:
        return self.db.query(ProductModel).filter(ProductModel.id == id).first()

    def find_all(self) -> list:
        return self.db.query(ProductModel).all()

    def find_by_category(self, category_id: uuid.UUID) -> list:
        return self.db.query(ProductModel).filter(ProductModel.category_id == category_id).all()

    def update(self, product: DomainProduct) -> ProductModel:
        db_product = self.db.query(ProductModel).filter(ProductModel.id == product.id).first()
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.stock_quantity = product.stock_quantity
        db_product.category_id = product.category_id
        db_product.is_active = product.is_active
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete(self, id: uuid.UUID) -> None:
        self.db.query(ProductModel).filter(ProductModel.id == id).delete()
        self.db.commit()
