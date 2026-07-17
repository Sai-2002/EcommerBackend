from fastapi import Depends 
from sqlalchemy.orm import Session

from ...infrastructure.session import get_db
from ...infrastructure.repository.user_repository import UserRepository
from ...application.use_cases.register import RegisterUseCase
from ...application.use_cases.login import LoginUseCase
from ..validators.auth_validator import RegisterRequest, LoginRequest

class AuthController:

    def register(self, request: RegisterRequest, db: Session = Depends(get_db)):
        # wire up dependencies
        user_repository = UserRepository(db)
        register_use_case = RegisterUseCase(user_repository)

        # execute
        result = register_use_case.execute(
            email=request.email,
            password=request.password
        )

        return result

    def login(self, request: LoginRequest, db: Session = Depends(get_db)):
        # wire up dependencies
        user_repository = UserRepository(db)
        login_use_case = LoginUseCase(user_repository)

        # execute
        result = login_use_case.execute(
            email=request.email,
            password=request.password
        )

        return result