from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.models.order import Order
from app.models.order_product import OrderProduct
from app.models.transition_log import TransitionLog
from typing import List, Dict, Optional
from uuid import UUID, uuid4


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, order_data: Dict, products: List[Dict]) -> Order:
        order = Order(
            id=uuid4(),
            amount=order_data["amount"],
            current_state=order_data["current_state"],
            customer_id=order_data["customer_id"],
            notes=order_data.get("notes")
        )
        self.db.add(order)
        await self.db.flush()

        for product in products:
            order_product = OrderProduct(
                order_id=order.id,
                product_id=product["product_id"],
                quantity=product["quantity"],
                unit_price=product["unit_price"]
            )
            self.db.add(order_product)

        initial_log = TransitionLog(
            id=uuid4(),
            order_id=order.id,
            previous_state=None,
            new_state=order_data["current_state"],
            action_taken="create"
        )
        self.db.add(initial_log)

        await self.db.commit()

        return await self.get_by_id(order.id)

    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        result = await self.db.execute(
            select(Order)
            .options(
                selectinload(Order.order_products).selectinload(OrderProduct.product),
                selectinload(Order.customer)
            )
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Order]:
        result = await self.db.execute(
            select(Order).options(
                selectinload(Order.order_products),
                selectinload(Order.customer)
            )
        )
        return list(result.scalars().all())

    async def delete(self, order_id: UUID) -> bool:
        result = await self.db.execute(
            select(Order).where(Order.id == order_id)
        )
        order = result.scalar_one_or_none()
        if order:
            await self.db.execute(
                delete(Order).where(Order.id == order_id)
            )
            await self.db.commit()
            return True
        return False

    async def update_state(self, order_id: UUID, new_state: str) -> Optional[Order]:
        order = await self.get_by_id(order_id)
        if order:
            order.current_state = new_state
            await self.db.commit()
            await self.db.refresh(order)
        return order