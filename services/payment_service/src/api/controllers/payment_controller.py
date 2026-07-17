from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from ...infrastructure.session import get_db
from ...infrastructure.repository.payment_repository import PaymentRepository
from ...application.use_cases.create_payment import CreatePaymentUseCase
from ...application.use_cases.get_payment import GetPaymentUseCase
from ...application.use_cases.get_payment_by_order import GetPaymentByOrderUseCase
from ..validators.payment_validator import CreatePaymentRequest


class PaymentController:

    def create_payment(self, request: CreatePaymentRequest, db: Session = Depends(get_db)):
        payment_repository = PaymentRepository(db)
        use_case = CreatePaymentUseCase(payment_repository)

        result = use_case.execute(
            order_id=str(request.order_id),
            user_id=str(request.user_id),
            amount=request.amount,
            payment_method=request.payment_method,
        )

        return result

    def get_payment(self, payment_id: UUID, db: Session = Depends(get_db)):
        payment_repository = PaymentRepository(db)
        use_case = GetPaymentUseCase(payment_repository)

        result = use_case.execute(payment_id=payment_id)

        return result

    def get_payment_by_order(self, order_id: UUID, db: Session = Depends(get_db)):
        payment_repository = PaymentRepository(db)
        use_case = GetPaymentByOrderUseCase(payment_repository)

        result = use_case.execute(order_id=order_id)

        return result
