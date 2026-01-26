from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.config.database import Base


class TransitionLog(Base):
    __tablename__ = "transition_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    previous_state = Column(String(50), nullable=True)  # Puede ser None en la creación inicial
    new_state = Column(String(50), nullable=False)
    action_taken = Column(String(50), nullable=False)
    transition_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    order = relationship("Order", backref="transition_logs")