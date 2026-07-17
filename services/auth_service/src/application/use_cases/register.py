from ...domain.entities.user import User
from ...domain.interfaces.user_repository import UserRepositoryInterface
from .token_helper import generate_token
import bcrypt

class RegisterUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, email: str, password: str) -> dict:
        # Step 1 — check if user already exists
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")

        # Step 2 — hash the password
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Step 3 — create entity (triggers validation)
        user = User(email=email, password=hashed_password)

        # Step 4 — save via repository
        saved_user = self.user_repository.save(user)

        # Step 5 — generate token and return
        token_data = generate_token(str(saved_user.id), saved_user.email)

        return {
            "user_id": str(saved_user.id),
            "email": saved_user.email,
            **token_data
        }