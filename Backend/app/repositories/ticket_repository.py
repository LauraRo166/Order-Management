from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.ticket import Ticket
from uuid import UUID
from typing import List, Optional


class TicketRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Ticket:
        ticket = Ticket(**data)
        self.db.add(ticket)
        await self.db.flush()
        await self.db.refresh(ticket)
        return ticket

    async def get_by_id(self, ticket_id: UUID) -> Optional[Ticket]:
        result = await self.db.execute(
            select(Ticket).where(Ticket.id == ticket_id)
        )
        return result.scalar_one_or_none()

    async def get_by_order_id(self, order_id: UUID) -> Optional[Ticket]:
        result = await self.db.execute(
            select(Ticket).where(Ticket.order_id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Ticket]:
        result = await self.db.execute(select(Ticket))
        return list(result.scalars().all())
