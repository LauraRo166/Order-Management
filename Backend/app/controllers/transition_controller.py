from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.repositories.order_repository import OrderRepository
from app.repositories.transition_log_repository import TransitionLogRepository
from app.services.transition_service import TransitionService
from app.services.state_machine import OrderStateMachine
from app.schemas.transition import TransitionRequest, TransitionLogResponse
from app.schemas.order import OrderResponse
from uuid import UUID
from typing import List

router = APIRouter(prefix="/orders", tags=["transitions"])


@router.get("/logs", response_model=List[TransitionLogResponse])
async def get_all_logs(
    db: AsyncSession = Depends(get_db),
    limit: int = 100
):
    log_repo = TransitionLogRepository(db)
    logs = await log_repo.get_all(limit=limit)
    return logs


@router.post("/{order_id}/transition", response_model=OrderResponse)
async def transition_order(
    order_id: UUID,
    transition_data: TransitionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Realiza una transición de estado en una orden.

    Esta operación es atómica: tanto el cambio de estado como el log
    se guardan en la misma transacción para garantizar consistencia.
    """
    order_repo = OrderRepository(db)
    log_repo = TransitionLogRepository(db)
    service = TransitionService(order_repo, log_repo)

    try:
        await service.transition_order(order_id, transition_data.action)

        # Obtener la orden actualizada con todas las relaciones
        updated_order = await order_repo.get_by_id(order_id)
        return updated_order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al realizar transición: {str(e)}")


@router.get("/{order_id}/logs", response_model=List[TransitionLogResponse])
async def get_order_logs(
    order_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    order_repo = OrderRepository(db)
    log_repo = TransitionLogRepository(db)
    service = TransitionService(order_repo, log_repo)

    try:
        logs = await service.get_order_logs(order_id)
        return logs
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{order_id}/allowed-actions", response_model=List[str])
async def get_allowed_actions(
    order_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Returns valid actions based on current state and business rules (e.g., amount > 1000 requires review)."""
    order_repo = OrderRepository(db)
    order = await order_repo.get_by_id(order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    allowed_actions = OrderStateMachine.get_allowed_actions(order.current_state)
    return allowed_actions

