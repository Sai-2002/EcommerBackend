from typing import Optional
import uuid
from sqlalchemy.orm import Session
from ..model.category import Category as CategoryModel
from ...domain.interfaces.category_repository import CategoryRepositoryInterface
from ...domain.entities.category import Category as DomainCategory


class CategoryRepository(CategoryRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def save(self, category: DomainCategory) -> CategoryModel:
        db_category = CategoryModel()
        db_category.id = category.id
        db_category.name = category.name
        db_category.description = category.description
        self.db.add(db_category)
        self.db.commit()
        self.db.refresh(db_category)
        return db_category

    def find_by_id(self, id: uuid.UUID) -> Optional[CategoryModel]:
        return self.db.query(CategoryModel).filter(CategoryModel.id == id).first()

    def find_all(self) -> list:
        return self.db.query(CategoryModel).all()
