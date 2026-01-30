from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.config.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Float, nullable=False)
    current_state = Column(String(50), nullable=False, default="pending")
    creation_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(Text, nullable=True)

    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)

    customer = relationship("Customer", back_populates="orders")
    order_products = relationship("OrderProduct", back_populates="order", cascade="all, delete-orphan")
    tickets = relationship("Ticket", back_populates="order", cascade="all, delete-orphan")
