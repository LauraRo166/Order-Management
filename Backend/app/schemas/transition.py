from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional


class TransitionRequest(BaseModel):
    action: str
    cancellation_reason: Optional[str] = None


class TransitionLogResponse(BaseModel):
    id: UUID
    order_id: UUID
    previous_state: Optional[str]
    new_state: str
    action_taken: str
    transition_date: datetime

    class Config:
        from_attributes = True