from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import TicketResponse
from uuid import UUID
from typing import List

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/", response_model=List[TicketResponse])
async def get_all_tickets(
    db: AsyncSession = Depends(get_db)
):
    ticket_repo = TicketRepository(db)
    tickets = await ticket_repo.get_all()
    return tickets


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    ticket_repo = TicketRepository(db)
    ticket = await ticket_repo.get_by_id(ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    return ticket


@router.get("/order/{order_id}", response_model=TicketResponse)
async def get_ticket_by_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    ticket_repo = TicketRepository(db)
    ticket = await ticket_repo.get_by_order_id(order_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="No se encontró ticket para esta orden")

    return ticket
