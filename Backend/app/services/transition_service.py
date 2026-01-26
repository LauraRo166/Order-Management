from app.repositories.order_repository import OrderRepository
from app.repositories.transition_log_repository import TransitionLogRepository
from app.services.state_machine import OrderStateMachine
from app.schemas.transition import TransitionLogResponse
from typing import List
from uuid import UUID


class TransitionService:
    def __init__(
        self,
        order_repo: OrderRepository,
        log_repo: TransitionLogRepository
    ):
        self.order_repo = order_repo
        self.log_repo = log_repo

    async def transition_order(self, order_id: UUID, action: str) -> dict:
        """
        Performs a state transition in one command.

        This operation is atomic: if it fails, neither the state change nor the transition log is saved.
        """

        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Order not found")

        is_valid, new_state, error_msg = OrderStateMachine.is_valid_transition(
            current_state=order.current_state,
            action=action,
            order_amount=order.amount
        )

        if not is_valid:
            raise ValueError(error_msg)

        previous_state = order.current_state

        order.current_state = new_state

        log_data = {
            "order_id": order.id,
            "previous_state": previous_state,
            "new_state": new_state,
            "action_taken": action
        }
        await self.log_repo.create(log_data)

        await self.log_repo.db.commit()
        await self.log_repo.db.refresh(order)

        return {
            "order_id": order.id,
            "previous_state": previous_state,
            "new_state": new_state,
            "action_taken": action
        }

    async def get_order_logs(self, order_id: UUID) -> List[TransitionLogResponse]:
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Order not found")

        logs = await self.log_repo.get_by_order_id(order_id)
        return [TransitionLogResponse.model_validate(log) for log in logs]