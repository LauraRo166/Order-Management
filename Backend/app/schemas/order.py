from pydantic import BaseModel, Field, computed_field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.schemas.customer import CustomerResponse
from app.schemas.product import ProductInOrder


class OrderCreate(BaseModel):
    amount: float = Field(..., gt=0)
    current_state: str = "pending"
    customer_id: UUID
    products: List[ProductInOrder]
    notes: Optional[str] = None


class OrderResponse(BaseModel):
    id: UUID
    amount: float
    current_state: str
    creation_date: datetime
    customer: CustomerResponse
    notes: Optional[str]

    class Config:
        from_attributes = True

    @computed_field
    @property
    def products(self) -> List[ProductInOrder]:
        """Convert order_products to the expected structure"""
        if not hasattr(self, 'order_products'):
            return []

        result = []
        for op in self.order_products:
            result.append(ProductInOrder(
                product_id=op.product_id,
                name=op.product.name if hasattr(op, 'product') and op.product else "Unknown",
                quantity=op.quantity,
                unit_price=op.unit_price
            ))
        return result
