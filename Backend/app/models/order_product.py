from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.config.database import Base


class OrderProduct(Base):
    __tablename__ = "order_products"

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), primary_key=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)  # 🆕 Precio en el momento de la orden

    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")