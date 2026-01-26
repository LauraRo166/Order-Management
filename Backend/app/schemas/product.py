from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal


class ProductCreate(BaseModel):
    name: str
    unit_price: float = Field(..., gt=0)


class ProductResponse(BaseModel):
    id: UUID
    name: str
    unit_price: float

    class Config:
        from_attributes = True


class ProductInOrder(BaseModel):
    product_id: UUID
    name: str
    quantity: int
    unit_price: Decimal

    class Config:
        from_attributes = True