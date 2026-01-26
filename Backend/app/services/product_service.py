from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductResponse
from typing import List
from uuid import UUID


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        product = await self.repository.create(product_data.model_dump())
        return ProductResponse.model_validate(product)

    async def get_product(self, product_id: UUID) -> ProductResponse:
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        return ProductResponse.model_validate(product)

    async def get_all_products(self) -> List[ProductResponse]:
        products = await self.repository.get_all()
        return [ProductResponse.model_validate(p) for p in products]