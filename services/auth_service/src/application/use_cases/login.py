import bcrypt
from ...domain.interfaces.user_repository import UserRepositoryInterface
from .token_helper import generate_token

class LoginUseCase:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    def execute(self, email: str, password: str) -> dict:
        # Step 1 — find user
        user = self.user_repository.find_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        # Step 2 — verify password
        password_matches = bcrypt.checkpw(
            password.encode("utf-8"),
            user.password.encode("utf-8")
        )
        if not password_matches:
            raise ValueError("Invalid email or password")

        # Step 3 — generate token and return
        token_data = generate_token(str(user.id), user.email)

        return {
            "user_id": str(user.id),
            "email": user.email,
            **token_data
        }