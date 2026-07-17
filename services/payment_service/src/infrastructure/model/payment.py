import uuid

from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from ..session import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    payment_method = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
