from pydantic import BaseModel, EmailStr
from uuid import UUID


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr


class CustomerResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr

    class Config:
        from_attributes = True