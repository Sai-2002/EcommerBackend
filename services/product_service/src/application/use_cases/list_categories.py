from ...domain.interfaces.category_repository import CategoryRepositoryInterface


class ListCategoriesUseCase:
    def __init__(self, category_repository: CategoryRepositoryInterface):
        self.category_repository = category_repository

    def execute(self) -> list:
        categories = self.category_repository.find_all()

        return [
            {
                "id": str(c.id),
                "name": c.name,
                "description": c.description,
            }
            for c in categories
        ]
