from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.repositories.customer_repository import CustomerRepository
from app.services.customer_service import CustomerService
from app.schemas.customer import CustomerCreate, CustomerResponse
from uuid import UUID

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=CustomerResponse, status_code=201)
async def create_customer(
    customer: CustomerCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        repository = CustomerRepository(db)
        service = CustomerService(repository)
        return await service.create_customer(customer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    try:
        repository = CustomerRepository(db)
        service = CustomerService(repository)
        return await service.get_customer(customer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))