import uuid
from ..model.user import User
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self,db:Session):
        self.db = db
        
    def create(self, email:str, password:str) -> User:
        user = User(email, password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def find_by_id(self, id: uuid.UUID) -> User | None:
        return self.db.query(User).filter(User.id == id).first()
