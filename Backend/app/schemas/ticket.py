from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class TicketCreate(BaseModel):
    order_id: UUID
    cancellation_reason: str


class TicketResponse(BaseModel):
    id: UUID
    order_id: UUID
    cancellation_reason: str
    creation_date: datetime

    class Config:
        from_attributes = True
