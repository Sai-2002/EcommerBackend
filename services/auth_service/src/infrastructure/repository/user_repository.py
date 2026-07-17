from typing import Optional
import uuid
from sqlalchemy.orm import Session
from ..model.user import User as UserModel
from ...domain.interfaces.user_repository import UserRepositoryInterface
from ...domain.entities.user import User as DomainUser


class UserRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def save(self, user: DomainUser) -> UserModel:
        db_user = UserModel()
        db_user.id = user.id
        db_user.email = user.email
        db_user.password = user.password
        db_user.isActive = user.isActive
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def find_by_email(self, email: str) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def find_by_id(self, id: uuid.UUID) -> Optional[UserModel]:
        return self.db.query(UserModel).filter(UserModel.id == id).first()
