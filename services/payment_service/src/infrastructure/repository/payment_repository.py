import uuid
from typing import Optional

from sqlalchemy.orm import Session

from ..model.payment import Payment as PaymentModel
from ...domain.interfaces.payment_repository import PaymentRepositoryInterface
from ...domain.entities.payment import Payment as DomainPayment


class PaymentRepository(PaymentRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def save(self, payment: DomainPayment) -> PaymentModel:
        db_payment = PaymentModel()
        db_payment.id = payment.id
        db_payment.order_id = payment.order_id
        db_payment.user_id = payment.user_id
        db_payment.amount = payment.amount
        db_payment.status = payment.status
        db_payment.payment_method = payment.payment_method
        self.db.add(db_payment)
        self.db.commit()
        self.db.refresh(db_payment)
        return db_payment

    def find_by_id(self, id: uuid.UUID) -> Optional[PaymentModel]:
        return self.db.query(PaymentModel).filter(PaymentModel.id == id).first()

    def find_by_order_id(self, order_id: uuid.UUID) -> Optional[PaymentModel]:
        return self.db.query(PaymentModel).filter(PaymentModel.order_id == order_id).first()
