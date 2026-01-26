from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerResponse
from uuid import UUID


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    async def create_customer(self, customer_data: CustomerCreate) -> CustomerResponse:
        existing = await self.repository.get_by_email(customer_data.email)
        if existing:
            return CustomerResponse.model_validate(existing)

        customer = await self.repository.create(customer_data.model_dump())
        return CustomerResponse.model_validate(customer)

    async def get_customer(self, customer_id: UUID) -> CustomerResponse:
        customer = await self.repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        return CustomerResponse.model_validate(customer)