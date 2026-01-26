from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.product import Product
from typing import Optional, List
from uuid import UUID


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, product_data: dict) -> Product:
        product = Product(**product_data)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Product]:
        result = await self.db.execute(select(Product))
        return result.scalars().all()