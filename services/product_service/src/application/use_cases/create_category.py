from ...domain.entities.category import Category
from ...domain.interfaces.category_repository import CategoryRepositoryInterface


class CreateCategoryUseCase:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    def execute(self, name: str, description: str = "") -> dict:
        # Create domain entity (triggers validation)
        category = Category(name=name, description=description)

        # Save via repository
        saved_category = self.category_repository.save(category)

        return {
            "id": str(saved_category.id),
            "name": saved_category.name,
            "description": saved_category.description,
        }
